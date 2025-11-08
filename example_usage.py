"""
Example usage of the MythoSciFi package.
"""

from mythoscifi import CharacterDatabase, NameGenerator


def main():
    print("="*80)
    print("MYTHOSCIFI PACKAGE DEMO")
    print("="*80)

    # Initialize database
    print("\n1. Initializing database...")
    db = CharacterDatabase(persist_directory="./chroma_db")
    db.initialize()

    # Get statistics
    stats = db.get_stats()
    print(f"\nDatabase contains:")
    print(f"  - Total: {stats['total']} characters")
    print(f"  - Robots: {stats['robots']}")
    print(f"  - Mythology: {stats['mythology']}")

    # Search for characters
    print("\n" + "="*80)
    print("2. Searching for 'goddess of wisdom'...")
    print("="*80)

    results = db.search("goddess of wisdom", n_results=5)
    for i, r in enumerate(results, 1):
        print(f"\n{i}. [{r['category'].upper()}] {r['name']}")
        print(f"   Description: {r['description'][:100]}...")
        print(f"   Similarity: {r['similarity']:.3f}")

    # Generate blended names
    print("\n" + "="*80)
    print("3. Generating blended names for 'powerful warrior'...")
    print("="*80)

    generator = NameGenerator(db)
    names = generator.generate(query="powerful warrior", top_n=5)

    for i, name in enumerate(names, 1):
        match = " ★ QUERY MATCH" if name.get('query_match', False) else ""
        print(f"\n{i}. {name['name']}{match}")
        print(f"   └─ Blend of: {name['source_myth']} + {name['source_robot']}")
        print(f"   └─ Creativity Score: {name['creativity_score']:.1f}")
        print(f"   └─ Similar to:")
        for j, m in enumerate(name['semantic_matches'][:3], 1):
            print(f"      {j}. [{m['category'].upper()}] {m['name']} ({m['similarity']:.3f})")

    print("\n" + "="*80)
    print("DEMO COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
