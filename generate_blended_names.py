import chromadb
import random
import sys


def load_collection(persist_directory="./chroma_db"):
    """Load the existing ChromaDB collection."""
    print("Loading ChromaDB...")
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_collection(name="characters")
    count = collection.count()
    print(f"✓ Loaded collection with {count} characters\n")
    return collection


def get_characters_by_category(collection, category, limit=100):
    """Get random characters from a specific category."""

    # Get all characters from the category
    results = collection.get(
        where={"category": category},
        limit=limit
    )

    characters = []
    for metadata in results['metadatas']:
        characters.append({
            'name': metadata['name'],
            'category': metadata['category']
        })

    return characters


def blend_names(myth_name, robot_name):
    """Create interesting blends of two names."""
    blends = []

    # Method 1: First half of myth + second half of robot
    if len(myth_name) > 2 and len(robot_name) > 2:
        mid1 = len(myth_name) // 2
        mid2 = len(robot_name) // 2
        blend1 = myth_name[:mid1] + robot_name[mid2:].lower()
        blends.append(blend1)

    # Method 2: First half of robot + second half of myth
    if len(robot_name) > 2 and len(myth_name) > 2:
        mid1 = len(robot_name) // 2
        mid2 = len(myth_name) // 2
        blend2 = robot_name[:mid1] + myth_name[mid2:].lower()
        blends.append(blend2)

    # Method 3: First 2/3 of myth + last 1/3 of robot
    if len(myth_name) > 3 and len(robot_name) > 3:
        cut1 = (len(myth_name) * 2) // 3
        cut2 = (len(robot_name) * 2) // 3
        blend3 = myth_name[:cut1] + robot_name[cut2:].lower()
        blends.append(blend3)

    # Method 4: Interleave syllables (simple version)
    if len(myth_name) > 4 and len(robot_name) > 4:
        blend4 = myth_name[:3] + robot_name[2:5].lower() + myth_name[-2:].lower()
        blends.append(blend4)

    # Method 5: Prefix from one, suffix from other
    if len(myth_name) > 3 and len(robot_name) > 3:
        blend5 = myth_name[:3] + robot_name[-4:].lower()
        blends.append(blend5)

    return blends


def is_pronounceable(word):
    """Check if a word is reasonably pronounceable."""
    word = word.lower()

    # Must be between 6 and 15 characters
    if len(word) < 6 or len(word) > 15:
        return False

    # Count consecutive consonants
    vowels = set('aeiouy')
    consonant_streak = 0
    vowel_streak = 0

    for char in word:
        if char in vowels:
            vowel_streak += 1
            consonant_streak = 0
            if vowel_streak > 3:  # Too many vowels in a row
                return False
        else:
            consonant_streak += 1
            vowel_streak = 0
            if consonant_streak > 3:  # Too many consonants in a row
                return False

    # Must have at least 2 vowels
    vowel_count = sum(1 for c in word if c in vowels)
    if vowel_count < 2:
        return False

    # Avoid weird character combinations
    weird_combos = ['xz', 'qx', 'zx', 'qz', 'xq', 'xxx', 'zzz']
    for combo in weird_combos:
        if combo in word:
            return False

    return True


def generate_unique_names(collection, num_samples=50, top_n=20):
    """Generate unique blended names from mythology and robot characters."""

    print("Fetching characters from database...")
    mythology_chars = get_characters_by_category(collection, "mythology", limit=num_samples)
    robot_chars = get_characters_by_category(collection, "robot", limit=num_samples)

    print(f"  - {len(mythology_chars)} mythology characters")
    print(f"  - {len(robot_chars)} robot characters")
    print("\nGenerating blended names...")

    all_blends = []

    # Create blends from random pairs
    random.shuffle(mythology_chars)
    random.shuffle(robot_chars)

    for i in range(min(len(mythology_chars), len(robot_chars))):
        myth_name = mythology_chars[i]['name']
        robot_name = robot_chars[i]['name']

        # Skip very short or very long names
        if len(myth_name) < 3 or len(robot_name) < 3:
            continue
        if len(myth_name) > 20 or len(robot_name) > 20:
            continue

        blends = blend_names(myth_name, robot_name)

        for blend in blends:
            if is_pronounceable(blend):
                all_blends.append({
                    'name': blend.capitalize(),
                    'source_myth': myth_name,
                    'source_robot': robot_name
                })

    print(f"Generated {len(all_blends)} pronounceable blended names\n")

    # Remove duplicates and select random sample
    unique_blends = {}
    for blend in all_blends:
        unique_blends[blend['name']] = blend

    # Get random selection
    selected = random.sample(list(unique_blends.values()), min(top_n, len(unique_blends)))

    return selected


def score_blend_creativity(blend_name, source_myth, source_robot):
    """Score how creative/unique a blend is."""
    score = 0

    # Longer names get bonus points (more interesting)
    score += len(blend_name) * 0.5

    # Names with good vowel/consonant balance
    vowels = sum(1 for c in blend_name.lower() if c in 'aeiouy')
    consonants = len(blend_name) - vowels
    ratio = vowels / len(blend_name)
    if 0.3 < ratio < 0.5:  # Good balance
        score += 5

    # Bonus for having parts from both sources clearly visible
    myth_overlap = sum(1 for i in range(len(source_myth)-1) if source_myth[i:i+2].lower() in blend_name.lower())
    robot_overlap = sum(1 for i in range(len(source_robot)-1) if source_robot[i:i+2].lower() in blend_name.lower())
    score += (myth_overlap + robot_overlap) * 2

    return score


def find_semantic_matches(collection, blend_name, n_results=3):
    """Find characters semantically similar to the blend name."""
    results = collection.query(
        query_texts=[blend_name],
        n_results=n_results
    )

    matches = []
    for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
        matches.append({
            'name': metadata['name'],
            'category': metadata['category'],
            'similarity': 1 - distance
        })

    return matches


def find_best_match_for_query(collection, query, scored_blends):
    """Find which blended names are most similar to the user's query."""

    print(f"\nFinding blended names similar to: '{query}'")
    print("-" * 80)

    # Search the blended names by querying the vector DB
    # We'll create a temporary collection with our blends
    query_scores = []

    for blend in scored_blends:
        # Create a simple similarity check by searching for the query
        # and seeing if our blend components match
        blend_text = f"{blend['name']} {blend['source_myth']} {blend['source_robot']}"

        # Get semantic matches for the blend
        matches = blend['semantic_matches']

        # Calculate relevance score based on semantic matches
        relevance = 0
        for match in matches:
            # If any semantic match is similar to our query, boost this blend
            similarity = match['similarity']
            relevance += similarity

        query_scores.append({
            **blend,
            'query_relevance': relevance
        })

    # Sort by query relevance
    query_scores.sort(key=lambda x: x['query_relevance'], reverse=True)

    return query_scores


def main():
    """Generate and display creative blended names."""

    collection = load_collection()

    # Check if user provided a query
    user_query = None
    if len(sys.argv) > 1:
        user_query = ' '.join(sys.argv[1:])
        print("="*80)
        print(f"GENERATING NAMES FOR QUERY: '{user_query}'")
        print("="*80)
        print("Combining Greek Mythology + Sci-Fi Robot names")
        print()
    else:
        print("="*80)
        print("GENERATING UNIQUE BLENDED NAMES")
        print("="*80)
        print("Combining Greek Mythology + Sci-Fi Robot names")
        print()

    # Generate candidates
    blends = generate_unique_names(collection, num_samples=100, top_n=30)

    # Score each blend
    print("Scoring creativity and finding semantic matches...")
    scored_blends = []

    for blend in blends:
        creativity_score = score_blend_creativity(
            blend['name'],
            blend['source_myth'],
            blend['source_robot']
        )

        # Find semantic matches
        if user_query:
            # Include the user query in semantic search
            matches = find_semantic_matches(collection, f"{user_query} {blend['name']}", n_results=3)
        else:
            matches = find_semantic_matches(collection, blend['name'], n_results=3)

        scored_blends.append({
            **blend,
            'creativity_score': creativity_score,
            'semantic_matches': matches
        })

    # If user provided a query, filter and sort by relevance to query
    if user_query:
        # First, get direct matches from the query
        print(f"\nSearching database for: '{user_query}'")
        query_results = collection.query(
            query_texts=[user_query],
            n_results=10
        )

        print(f"Found {len(query_results['metadatas'][0])} relevant characters")
        print("Filtering blended names based on these characters...\n")

        # Find blends that use these characters
        relevant_chars = set()
        for metadata in query_results['metadatas'][0]:
            relevant_chars.add(metadata['name'])

        # Filter blends that use relevant characters
        filtered_blends = []
        for blend in scored_blends:
            if blend['source_myth'] in relevant_chars or blend['source_robot'] in relevant_chars:
                blend['query_match'] = True
                filtered_blends.append(blend)

        # If we found query-matched blends, prioritize them
        if filtered_blends:
            print(f"Found {len(filtered_blends)} blended names using characters matching your query!\n")
            scored_blends = filtered_blends + [b for b in scored_blends if b not in filtered_blends]

        # Sort by creativity score
        scored_blends.sort(key=lambda x: (x.get('query_match', False), x['creativity_score']), reverse=True)
    else:
        # Sort by creativity score
        scored_blends.sort(key=lambda x: x['creativity_score'], reverse=True)

    # Display top 5
    print("\n" + "="*80)
    if user_query:
        print(f"TOP 5 BLENDED NAMES FOR: '{user_query}'")
    else:
        print("TOP 5 UNIQUE BLENDED NAMES")
    print("="*80)
    print()

    for i, blend in enumerate(scored_blends[:5], 1):
        match_indicator = " ★ QUERY MATCH" if blend.get('query_match', False) else ""
        print(f"{i}. {blend['name']}{match_indicator}")
        print(f"   └─ Blend of: {blend['source_myth']} (mythology) + {blend['source_robot']} (robot)")
        print(f"   └─ Creativity Score: {blend['creativity_score']:.1f}")
        print(f"   └─ Semantically similar to:")

        for j, match in enumerate(blend['semantic_matches'], 1):
            print(f"      {j}. [{match['category'].upper()}] {match['name']} (similarity: {match['similarity']:.3f})")
        print()

    # Show more options
    print("\n" + "="*80)
    print("HONORABLE MENTIONS (Names 6-15)")
    print("="*80)
    print()

    for i, blend in enumerate(scored_blends[5:15], 6):
        match_indicator = " ★" if blend.get('query_match', False) else ""
        print(f"{i}. {blend['name']}{match_indicator} - from {blend['source_myth']} + {blend['source_robot']}")

    print("\n" + "="*80)
    if user_query:
        print(f"Blended names tailored to: '{user_query}'")
    else:
        print("All names are pronounceable blends of mythology and sci-fi robot names!")
    print("Usage: python generate_blended_names.py \"your query here\"")
    print("="*80)


if __name__ == "__main__":
    main()
