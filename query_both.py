import chromadb
import sys


def load_collection(persist_directory="./chroma_db"):
    """Load the existing ChromaDB collection."""

    print("Loading ChromaDB...")
    client = chromadb.PersistentClient(path=persist_directory)

    try:
        collection = client.get_collection(name="characters")
        count = collection.count()
        print(f"✓ Loaded collection with {count} characters\n")
        return collection
    except Exception as e:
        print(f"Error: Could not load collection. Make sure you've run store_both_in_chroma.py first!")
        print(f"Error details: {e}")
        return None


def search_characters(collection, query, n_results=5, filter_category=None):
    """Search for characters similar to the query and return top N results."""

    print(f"Query: '{query}'")
    if filter_category:
        print(f"Filter: {filter_category} only")
    print("="*80)

    # Build the query
    query_kwargs = {
        "query_texts": [query],
        "n_results": n_results
    }

    # Add filter if specified
    if filter_category:
        query_kwargs["where"] = {"category": filter_category}

    results = collection.query(**query_kwargs)

    if not results['documents'][0]:
        print("No results found!")
        return

    print(f"\nTop {n_results} Results:\n")

    for i, (metadata, distance) in enumerate(zip(
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        similarity = 1 - distance

        print(f"{i}. [{metadata['category'].upper()}] {metadata['name']}")
        print(f"   Description: {metadata['description'][:200]}...")
        print(f"   Similarity: {similarity:.3f}")
        print()

    return results


def interactive_mode(collection):
    """Run interactive search mode where user can enter queries."""

    print("\n" + "="*80)
    print("INTERACTIVE SEARCH MODE")
    print("="*80)
    print("Enter your search queries to find similar characters.")
    print("Commands:")
    print("  - Type your query to search all categories")
    print("  - Type 'robot: query' to search only robots")
    print("  - Type 'mythology: query' to search only mythology")
    print("  - Type 'quit' or 'exit' to stop\n")

    while True:
        try:
            query = input("Search query: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if not query:
                print("Please enter a query.\n")
                continue

            # Check for category filter
            filter_category = None
            if query.startswith("robot:"):
                filter_category = "robot"
                query = query[6:].strip()
            elif query.startswith("mythology:"):
                filter_category = "mythology"
                query = query[10:].strip()

            print()
            search_characters(collection, query, n_results=5, filter_category=filter_category)
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

        # Check for category filter in command line
        filter_category = None
        if query.startswith("robot:"):
            filter_category = "robot"
            query = query[6:].strip()
        elif query.startswith("mythology:"):
            filter_category = "mythology"
            query = query[10:].strip()

        search_characters(collection, query, n_results=5, filter_category=filter_category)
    else:
        # Run predefined test queries
        print("="*80)
        print("RUNNING TEST QUERIES")
        print("="*80)
        print()

        test_queries = [
            ("powerful god or deity", None),
            ("brave warrior hero", None),
            ("intelligent robot with AI", "robot"),
            ("goddess of wisdom", "mythology"),
            ("evil killer machine", "robot"),
            ("thunder and lightning", None),
        ]

        for query, filter_cat in test_queries:
            search_characters(collection, query, n_results=5, filter_category=filter_cat)
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
