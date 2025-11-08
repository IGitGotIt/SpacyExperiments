import chromadb
from chromadb.config import Settings
import requests
from bs4 import BeautifulSoup


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

    # Extract robot names from all list items and tables
    robots = []

    # Try to find robot names in list format (often in alphabetical sections)
    content = soup.find('div', class_='mw-parser-output')

    if content:
        current_section = None
        for element in content.find_all(['h2', 'h3', 'ul', 'table']):
            if element.name in ['h2', 'h3']:
                current_section = element.get_text(strip=True)

            elif element.name == 'ul':
                for li in element.find_all('li', recursive=False):
                    text = li.get_text(separator=' ', strip=True)
                    # Try to extract robot name (usually before first dash or parenthesis)
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
                            'description': desc[:500]  # Keep more description for better embeddings
                        })

    return robots


def store_in_chromadb(robots, persist_directory="./chroma_db"):
    """Store robot data in ChromaDB with persistence."""

    print(f"\nInitializing ChromaDB (persisting to {persist_directory})...")

    # Create a persistent Chroma client
    client = chromadb.PersistentClient(path=persist_directory)

    # Get or create a collection for robots
    # Delete collection if it exists (for fresh start)
    try:
        client.delete_collection(name="scifi_robots")
        print("Deleted existing collection")
    except:
        pass

    collection = client.create_collection(
        name="scifi_robots",
        metadata={"description": "Fictional robots and androids from Wikipedia"}
    )

    print(f"\nStoring {len(robots)} robots in ChromaDB...")

    # Prepare data for batch insert
    documents = []
    metadatas = []
    ids = []

    for i, robot in enumerate(robots):
        # Create a rich document combining name and description
        doc = f"Name: {robot['name']}\nDescription: {robot['description']}"
        documents.append(doc)

        # Store metadata
        metadatas.append({
            "name": robot['name'],
            "description": robot['description']
        })

        # Create unique ID
        ids.append(f"robot_{i}")

    # Add all documents to the collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully stored {len(robots)} robots in ChromaDB!")
    print(f"Database persisted to: {persist_directory}")

    return collection


def search_robots(collection, query, n_results=5):
    """Search for robots similar to the query."""

    print(f"\nSearching for: '{query}'")
    print("-" * 80)

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    print(f"\nFound {len(results['documents'][0])} results:\n")

    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        print(f"{i}. {metadata['name']}")
        print(f"   Description: {metadata['description'][:150]}...")
        print(f"   Similarity score: {1 - distance:.3f}")  # Convert distance to similarity
        print()

    return results


def main():
    """Main function to fetch, store, and search robot data."""

    # Fetch robot data from Wikipedia
    print("="*80)
    print("SCRAPING WIKIPEDIA FOR ROBOT DATA")
    print("="*80)
    robots = fetch_wikipedia_robots()

    if not robots:
        print("No robots found!")
        return

    print(f"Fetched {len(robots)} robots from Wikipedia")

    # Store in ChromaDB
    print("\n" + "="*80)
    print("STORING IN CHROMADB")
    print("="*80)
    collection = store_in_chromadb(robots)

    # Example searches
    print("\n" + "="*80)
    print("EXAMPLE SEARCHES")
    print("="*80)

    # Search for different types of robots
    search_robots(collection, "friendly robot companion", n_results=5)
    search_robots(collection, "evil AI or terminator", n_results=5)
    search_robots(collection, "android or humanoid robot", n_results=5)

    print("\n" + "="*80)
    print("Database ready! You can now query it anytime.")
    print("="*80)


if __name__ == "__main__":
    main()
