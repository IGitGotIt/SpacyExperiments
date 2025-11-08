import chromadb

# Create a simple in-memory Chroma client
print("Creating ChromaDB client...")
client = chromadb.Client()

# Create a collection
print("Creating a test collection...")
collection = client.create_collection(name="test_collection")

# Add some test documents
print("Adding test documents...")
collection.add(
    documents=["This is a test document", "This is another test document"],
    ids=["doc1", "doc2"],
    metadatas=[{"source": "test"}, {"source": "test"}]
)

# Query the collection
print("Querying the collection...")
results = collection.query(
    query_texts=["test document"],
    n_results=2
)

print("\n✓ ChromaDB is working correctly!")
print(f"\nQuery Results:")
print(f"Documents found: {results['documents']}")
print(f"IDs: {results['ids']}")
print(f"Distances: {results['distances']}")
