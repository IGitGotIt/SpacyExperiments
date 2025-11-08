"""
Command-line interface for MythoSciFi package.
"""

import sys
from .database import CharacterDatabase
from .name_generator import NameGenerator


def populate_database():
    """CLI command to populate the database."""
    print("="*80)
    print("POPULATING MYTHOSCIFI DATABASE")
    print("="*80)

    db = CharacterDatabase()
    db.initialize()
    db.populate()

    stats = db.get_stats()
    print("\n" + "="*80)
    print("DATABASE POPULATED SUCCESSFULLY")
    print(f"Total: {stats['total']} characters")
    print(f"  - Robots: {stats['robots']}")
    print(f"  - Mythology: {stats['mythology']}")
    print("="*80)


def search_characters():
    """CLI command to search for characters."""
    if len(sys.argv) < 2:
        print("Usage: mythoscifi-search <query>")
        print("Example: mythoscifi-search 'goddess of wisdom'")
        return

    query = ' '.join(sys.argv[1:])

    db = CharacterDatabase()
    db.initialize()

    print("="*80)
    print(f"SEARCHING FOR: '{query}'")
    print("="*80)

    results = db.search(query, n_results=10)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. [{result['category'].upper()}] {result['name']}")
        print(f"   {result['description'][:150]}...")
        print(f"   Similarity: {result['similarity']:.3f}")

    print("\n" + "="*80)


def generate_names():
    """CLI command to generate blended names."""
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else None

    db = CharacterDatabase()
    db.initialize()
    generator = NameGenerator(db)

    print("="*80)
    if query:
        print(f"GENERATING NAMES FOR: '{query}'")
    else:
        print("GENERATING RANDOM BLENDED NAMES")
    print("="*80)

    names = generator.generate(query=query, top_n=5)

    for i, name in enumerate(names, 1):
        match_indicator = " ★" if name.get('query_match', False) else ""
        print(f"\n{i}. {name['name']}{match_indicator}")
        print(f"   └─ From: {name['source_myth']} (mythology) + {name['source_robot']} (robot)")
        print(f"   └─ Creativity: {name['creativity_score']:.1f}")
        print(f"   └─ Similar to:")
        for j, match in enumerate(name['semantic_matches'][:3], 1):
            print(f"      {j}. [{match['category'].upper()}] {match['name']}")

    print("\n" + "="*80)
    print("Usage: mythoscifi-generate [query]")
    print("="*80)
