"""
Example usage of the MythologyCountVectorizer class.
"""

from CntVector import MythologyCountVectorizer


def example_basic_usage():
    """Basic usage example."""
    print("="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)

    # Initialize and load
    mvc = MythologyCountVectorizer()
    mvc.load_characters()

    # Create DTM with 20 bigrams
    mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

    # Get top bigrams
    top_bigrams = mvc.get_most_common_bigrams(top_n=10)
    print("\nTop 10 Bigrams:")
    for bigram, count in top_bigrams:
        print(f"  '{bigram}': {count}")


def example_character_analysis():
    """Analyze specific characters."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Character Analysis")
    print("="*80)

    mvc = MythologyCountVectorizer()
    mvc.load_characters()
    mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

    # Analyze Zeus
    analysis = mvc.analyze_character('Zeus')

    print(f"\nCharacter: {analysis['name']}")
    print(f"Description: {analysis['description']}")
    print(f"\nTop Bigrams:")
    for bigram, count in analysis['top_bigrams']:
        print(f"  - '{bigram}': {count}")

    print(f"\nSimilar Characters:")
    for name, score in analysis['similar_characters']:
        print(f"  - {name}: {score:.3f}")


def example_compare_characters():
    """Compare multiple characters."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Compare Multiple Characters")
    print("="*80)

    mvc = MythologyCountVectorizer()
    mvc.load_characters()
    mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

    characters = ['Zeus', 'Poseidon', 'Hades', 'Athena', 'Apollo']

    for char_name in characters:
        top_bigrams = mvc.get_top_bigrams_per_character(char_name, top_n=3)
        print(f"\n{char_name}:")
        for bigram, count in top_bigrams:
            print(f"  - '{bigram}': {count}")


def example_custom_ngrams():
    """Try different n-gram configurations."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Custom N-grams")
    print("="*80)

    mvc = MythologyCountVectorizer()
    mvc.load_characters()

    # Try unigrams (single words)
    print("\nUsing UNIGRAMS (1-word):")
    mvc.create_document_term_matrix(max_features=15, ngram_range=(1, 1))
    top_unigrams = mvc.get_most_common_bigrams(top_n=10)
    for word, count in top_unigrams:
        print(f"  '{word}': {count}")

    # Try trigrams (3-word combinations)
    print("\nUsing TRIGRAMS (3-word):")
    mvc.create_document_term_matrix(max_features=15, ngram_range=(3, 3))
    top_trigrams = mvc.get_most_common_bigrams(top_n=10)
    for phrase, count in top_trigrams:
        print(f"  '{phrase}': {count}")


def example_dataframe_export():
    """Export to pandas DataFrame."""
    print("\n" + "="*80)
    print("EXAMPLE 5: DataFrame Export")
    print("="*80)

    mvc = MythologyCountVectorizer()
    mvc.load_characters()
    mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

    # Get as DataFrame
    df = mvc.get_dtm_dataframe(top_n=10)

    print("\nDocument-Term Matrix (first 10 characters):")
    print(df)

    # Show row sums (total bigrams per character)
    print("\nTotal bigrams per character:")
    row_sums = df.sum(axis=1)
    print(row_sums)

    # Show column sums (total occurrences per bigram)
    print("\nTotal occurrences per bigram:")
    col_sums = df.sum(axis=0)
    print(col_sums.head(10))


def example_find_similar():
    """Find similar characters based on bigrams."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Find Similar Characters")
    print("="*80)

    mvc = MythologyCountVectorizer()
    mvc.load_characters()
    mvc.create_document_term_matrix(max_features=30, ngram_range=(2, 2))

    test_characters = ['Zeus', 'Athena', 'Hercules', 'Achilles']

    for char in test_characters:
        similar = mvc.find_similar_characters(char, top_n=5)
        print(f"\n{char} is similar to:")
        for name, score in similar:
            print(f"  - {name}: {score:.3f}")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("MYTHOLOGY COUNT VECTORIZER - EXAMPLES")
    print("="*80)

    example_basic_usage()
    example_character_analysis()
    example_compare_characters()
    example_custom_ngrams()
    example_dataframe_export()
    example_find_similar()

    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED!")
    print("="*80)


if __name__ == "__main__":
    main()
