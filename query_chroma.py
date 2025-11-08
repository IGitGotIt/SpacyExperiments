import chromadb
import sys


def load_collection(persist_directory="./chroma_db"):
    """Load the existing ChromaDB collection."""

    print("Loading ChromaDB...")
    client = chromadb.PersistentClient(path=persist_directory)

    try:
        collection = client.get_collection(name="scifi_robots")
        count = collection.count()
        print(f"✓ Loaded collection with {count} robots\n")
        return collection
    except Exception as e:
        print(f"Error: Could not load collection. Make sure you've run store_in_chroma.py first!")
        print(f"Error details: {e}")
        return None


def search_robots(collection, query, n_results=5):
    """Search for robots similar to the query and return top N results."""

    print(f"Query: '{query}'")
    print("="*80)

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if not results['documents'][0]:
        print("No results found!")
        return

    print(f"\nTop {n_results} Results:\n")

    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        similarity = 1 - distance  # Convert distance to similarity score

        print(f"{i}. {metadata['name']}")
        print(f"   Description: {metadata['description'][:200]}...")
        print(f"   Similarity: {similarity:.3f} (distance: {distance:.3f})")
        print()

    return results


def interactive_mode(collection):
    """Run interactive search mode where user can enter queries."""

    print("\n" + "="*80)
    print("INTERACTIVE SEARCH MODE")
    print("="*80)
    print("Enter your search queries to find similar robots.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            query = input("Search query: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if not query:
                print("Please enter a query.\n")
                continue

            print()
            search_robots(collection, query, n_results=5)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


def main():
    """Main function to query the ChromaDB."""

    # Load the collection
    collection = load_collection()

    if not collection:
        return

    # Check if a query was provided as command line argument
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        search_robots(collection, query, n_results=5)
    else:
        # Run predefined test queries
        print("="*80)
        print("RUNNING TEST QUERIES")
        print("="*80)
        print()

        test_queries = [
            "robot with artificial intelligence",
            "space exploration robot",
            "evil killer robot",
            "helpful assistant droid",
            "time traveling robot"
        ]

        for query in test_queries:
            search_robots(collection, query, n_results=5)
            print("\n" + "-"*80 + "\n")

        # Offer interactive mode (only if running in a terminal)
        try:
            response = input("\nWould you like to enter interactive search mode? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                interactive_mode(collection)
        except EOFError:
            print("\nTest queries completed!")
            pass


if __name__ == "__main__":
    main()
