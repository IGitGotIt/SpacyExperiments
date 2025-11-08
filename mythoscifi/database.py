"""
Database module for storing and querying characters.
"""

import chromadb
import requests
from bs4 import BeautifulSoup
import kagglehub
import pandas as pd
import os


class CharacterDatabase:
    """Manages the ChromaDB vector database for characters."""

    def __init__(self, persist_directory="./chroma_db"):
        """
        Initialize the character database.

        Args:
            persist_directory: Path where the database will be persisted
        """
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None

    def initialize(self):
        """Initialize the ChromaDB client and load collection."""
        print(f"Initializing ChromaDB at {self.persist_directory}...")
        self.client = chromadb.PersistentClient(path=self.persist_directory)

        try:
            self.collection = self.client.get_collection(name="characters")
            count = self.collection.count()
            print(f"✓ Loaded existing collection with {count} characters")
        except:
            print("No existing collection found. Use populate() to create one.")
            self.collection = None

        return self

    def populate(self, fetch_robots=True, fetch_mythology=True, num_samples=None):
        """
        Populate the database with characters.

        Args:
            fetch_robots: Whether to fetch robot characters
            fetch_mythology: Whether to fetch mythology characters
            num_samples: Limit number of samples (None for all)
        """
        all_data = []

        if fetch_robots:
            print("\nFetching Sci-Fi Robots from Wikipedia...")
            robots = self._fetch_robots()
            print(f"✓ Fetched {len(robots)} robots")
            all_data.extend(robots)

        if fetch_mythology:
            print("\nFetching Greek Mythology Characters from Kaggle...")
            mythology = self._fetch_mythology()
            print(f"✓ Fetched {len(mythology)} mythology characters")
            all_data.extend(mythology)

        if num_samples and num_samples < len(all_data):
            import random
            all_data = random.sample(all_data, num_samples)

        print(f"\nTotal characters to store: {len(all_data)}")
        self._store_characters(all_data)

        return self

    def _fetch_robots(self):
        """Fetch robot data from Wikipedia."""
        url = "https://en.wikipedia.org/wiki/List_of_fictional_robots_and_androids"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        robots = []
        content = soup.find('div', class_='mw-parser-output')

        if content:
            for element in content.find_all('ul'):
                for li in element.find_all('li', recursive=False):
                    text = li.get_text(separator=' ', strip=True)
                    if ' – ' in text:
                        name, desc = text.split(' – ', 1)
                    elif ' - ' in text:
                        name, desc = text.split(' - ', 1)
                    else:
                        name = text.split('(')[0].strip() if '(' in text else text
                        desc = text

                    if name and len(name) > 1:
                        robots.append({
                            'name': name,
                            'description': desc[:500],
                            'category': 'robot'
                        })

        return robots

    def _fetch_mythology(self):
        """Fetch Greek mythology data from Kaggle."""
        path = kagglehub.dataset_download("zaylaatsi/greek-mythology-network-data")
        characters_file = os.path.join(path, 'characters.csv')
        df = pd.read_csv(characters_file)

        characters = []
        for _, row in df.iterrows():
            name = row['name']
            description = row['description'] if pd.notna(row['description']) else 'Greek mythology character'
            characters.append({
                'name': name,
                'description': str(description)[:500],
                'category': 'mythology'
            })

        return characters

    def _store_characters(self, characters):
        """Store characters in ChromaDB."""
        if not self.client:
            self.initialize()

        # Delete existing collection
        try:
            self.client.delete_collection(name="characters")
        except:
            pass

        # Create new collection
        self.collection = self.client.create_collection(
            name="characters",
            metadata={"description": "Fictional characters: Sci-fi robots and Greek mythology"}
        )

        print(f"Storing {len(characters)} characters...")

        documents = []
        metadatas = []
        ids = []

        for i, char in enumerate(characters):
            doc = f"Name: {char['name']}\nCategory: {char['category']}\nDescription: {char['description']}"
            documents.append(doc)
            metadatas.append(char)
            ids.append(f"{char['category']}_{i}")

        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"✓ Successfully stored {len(characters)} characters")

    def search(self, query, n_results=5, filter_category=None):
        """
        Search for characters similar to the query.

        Args:
            query: Search query string
            n_results: Number of results to return
            filter_category: Filter by 'robot' or 'mythology' (None for all)

        Returns:
            Dictionary with search results
        """
        if not self.collection:
            raise Exception("Database not initialized. Call initialize() first.")

        query_kwargs = {
            "query_texts": [query],
            "n_results": n_results
        }

        if filter_category:
            query_kwargs["where"] = {"category": filter_category}

        results = self.collection.query(**query_kwargs)

        formatted_results = []
        for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
            formatted_results.append({
                'name': metadata['name'],
                'category': metadata['category'],
                'description': metadata['description'],
                'similarity': 1 - distance,
                'distance': distance
            })

        return formatted_results

    def get_random_characters(self, category=None, limit=100):
        """
        Get random characters from the database.

        Args:
            category: Filter by category ('robot' or 'mythology')
            limit: Maximum number of characters to return

        Returns:
            List of character dictionaries
        """
        if not self.collection:
            raise Exception("Database not initialized. Call initialize() first.")

        if category:
            results = self.collection.get(where={"category": category}, limit=limit)
        else:
            results = self.collection.get(limit=limit)

        characters = []
        for metadata in results['metadatas']:
            characters.append({
                'name': metadata['name'],
                'category': metadata['category'],
                'description': metadata['description']
            })

        return characters

    def get_stats(self):
        """Get database statistics."""
        if not self.collection:
            return {"error": "Database not initialized"}

        total = self.collection.count()
        robots = len(self.collection.get(where={"category": "robot"}, limit=10000)['ids'])
        mythology = len(self.collection.get(where={"category": "mythology"}, limit=10000)['ids'])

        return {
            'total': total,
            'robots': robots,
            'mythology': mythology
        }
