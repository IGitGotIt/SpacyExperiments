import chromadb
import requests
from bs4 import BeautifulSoup
import kagglehub
import pandas as pd
import os


def fetch_wikipedia_robots():
    """Fetch the list of fictional robots and androids from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_fictional_robots_and_androids"

    print(f"Fetching data from: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    robots = []
    content = soup.find('div', class_='mw-parser-output')

    if content:
        for element in content.find_all(['h2', 'h3', 'ul', 'table']):
            if element.name == 'ul':
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


def fetch_greek_mythology_characters():
    """Fetch Greek mythology characters from Kaggle dataset."""
    print("\nDownloading Greek mythology dataset from Kaggle...")
    path = kagglehub.dataset_download("zaylaatsi/greek-mythology-network-data")

    characters_file = os.path.join(path, 'characters.csv')
    df = pd.read_csv(characters_file)

    print(f"Loaded {len(df)} Greek mythology characters")

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


def store_in_chromadb(all_data, persist_directory="./chroma_db"):
    """Store both robots and mythology characters in ChromaDB."""

    print(f"\nInitializing ChromaDB (persisting to {persist_directory})...")
    client = chromadb.PersistentClient(path=persist_directory)

    # Delete existing collections if they exist
    try:
        client.delete_collection(name="scifi_robots")
        print("Deleted existing 'scifi_robots' collection")
    except:
        pass

    try:
        client.delete_collection(name="characters")
        print("Deleted existing 'characters' collection")
    except:
        pass

    # Create a single collection for all characters
    collection = client.create_collection(
        name="characters",
        metadata={"description": "Fictional characters: Sci-fi robots and Greek mythology"}
    )

    print(f"\nStoring {len(all_data)} characters in ChromaDB...")

    # Prepare data for batch insert
    documents = []
    metadatas = []
    ids = []

    for i, item in enumerate(all_data):
        # Create a rich document
        doc = f"Name: {item['name']}\nCategory: {item['category']}\nDescription: {item['description']}"
        documents.append(doc)

        # Store metadata
        metadatas.append({
            "name": item['name'],
            "description": item['description'],
            "category": item['category']
        })

        # Create unique ID
        ids.append(f"{item['category']}_{i}")

    # Add all documents to the collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully stored {len(all_data)} characters in ChromaDB!")
    print(f"  - Robots: {sum(1 for x in all_data if x['category'] == 'robot')}")
    print(f"  - Mythology: {sum(1 for x in all_data if x['category'] == 'mythology')}")
    print(f"Database persisted to: {persist_directory}")

    return collection


def search_characters(collection, query, n_results=5, filter_category=None):
    """Search for characters similar to the query."""

    print(f"\nSearching for: '{query}'")
    if filter_category:
        print(f"Filter: {filter_category} only")
    print("-" * 80)

    # Build the query
    query_kwargs = {
        "query_texts": [query],
        "n_results": n_results
    }

    # Add filter if specified
    if filter_category:
        query_kwargs["where"] = {"category": filter_category}

    results = collection.query(**query_kwargs)

    print(f"\nFound {len(results['documents'][0])} results:\n")

    for i, (metadata, distance) in enumerate(zip(
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        similarity = 1 - distance
        print(f"{i}. [{metadata['category'].upper()}] {metadata['name']}")
        print(f"   Description: {metadata['description'][:150]}...")
        print(f"   Similarity: {similarity:.3f}")
        print()

    return results


def main():
    """Main function to fetch, store, and search both datasets."""

    print("="*80)
    print("COLLECTING DATA")
    print("="*80)

    # Fetch robots
    print("\n1. Fetching Sci-Fi Robots from Wikipedia...")
    robots = fetch_wikipedia_robots()
    print(f"   ✓ Fetched {len(robots)} robots")

    # Fetch Greek mythology characters
    print("\n2. Fetching Greek Mythology Characters from Kaggle...")
    mythology = fetch_greek_mythology_characters()
    print(f"   ✓ Fetched {len(mythology)} mythology characters")

    # Combine both datasets
    all_data = robots + mythology
    print(f"\n   Total characters: {len(all_data)}")

    # Store in ChromaDB
    print("\n" + "="*80)
    print("STORING IN CHROMADB")
    print("="*80)
    collection = store_in_chromadb(all_data)

    # Example searches
    print("\n" + "="*80)
    print("EXAMPLE SEARCHES")
    print("="*80)

    # Search across both categories
    search_characters(collection, "powerful warrior", n_results=5)
    search_characters(collection, "god of the sea", n_results=5)
    search_characters(collection, "friendly robot companion", n_results=5)

    # Search with filters
    search_characters(collection, "hero", n_results=5, filter_category="mythology")
    search_characters(collection, "intelligent machine", n_results=5, filter_category="robot")

    print("\n" + "="*80)
    print("Database ready! Use query_chroma.py to search.")
    print("="*80)


if __name__ == "__main__":
    main()
