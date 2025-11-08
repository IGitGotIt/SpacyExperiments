# Count Vectorization for Mythology Characters

This module provides count vectorization analysis of Greek mythology character descriptions using scikit-learn's CountVectorizer with bigram (2-word) features.

## Overview

**CntVector.py** creates a Document-Term Matrix (DTM) where:
- **Documents** = Character descriptions (1,076 mythology characters)
- **Terms** = Bigrams (2-word combinations) from descriptions
- **Matrix values** = Count of each bigram in each description

## Features

✓ Load mythology characters from ChromaDB vector database
✓ Create document-term matrix with configurable n-grams
✓ Find most common bigrams across all characters
✓ Analyze individual characters' bigram profiles
✓ Find similar characters using cosine similarity
✓ Export to pandas DataFrame and CSV
✓ Support for unigrams, bigrams, and trigrams

## Quick Start

```python
from CntVector import MythologyCountVectorizer

# Initialize
mvc = MythologyCountVectorizer()
mvc.load_characters()

# Create DTM with 20 bigrams
mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

# Get top bigrams
top_bigrams = mvc.get_most_common_bigrams(top_n=10)
for bigram, count in top_bigrams:
    print(f"'{bigram}': {count}")
```

## Results from Analysis

### Top 20 Bigrams in Mythology Descriptions

1. **'greek mythology'** - 453 occurrences
2. **'mythical character'** - 60 occurrences
3. **'mythical son'** - 47 occurrences
4. **'greek mythological'** - 43 occurrences
5. **'ancient greek'** - 36 occurrences
6. **'greek goddess'** - 33 occurrences
7. **'mythical king'** - 32 occurrences
8. **'mythological figure'** - 23 occurrences
9. **'character son'** - 23 occurrences
10. **'king sparta'** - 20 occurrences

### Document-Term Matrix Statistics

- **Shape**: (1,076 documents × 20 features)
- **Sparsity**: 95.71% (most entries are zero)
- **Characters analyzed**: 1,076 Greek mythology characters
- **Feature type**: Bigrams (2-word combinations)

## API Reference

### MythologyCountVectorizer Class

#### `__init__(persist_directory="./chroma_db")`
Initialize the vectorizer with ChromaDB path.

#### `load_characters()`
Load mythology characters from the vector database.

```python
mvc = MythologyCountVectorizer()
mvc.load_characters()
# Returns: self (for method chaining)
```

#### `create_document_term_matrix(max_features=20, ngram_range=(2, 2))`
Create the document-term matrix.

**Parameters:**
- `max_features`: Number of top features to keep (default: 20)
- `ngram_range`: Tuple (min_n, max_n) for n-gram range
  - `(1, 1)` = unigrams (single words)
  - `(2, 2)` = bigrams (2-word combinations)
  - `(3, 3)` = trigrams (3-word combinations)
  - `(1, 2)` = unigrams + bigrams

```python
# Bigrams with 20 features
mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

# Unigrams with 30 features
mvc.create_document_term_matrix(max_features=30, ngram_range=(1, 1))

# Trigrams with 15 features
mvc.create_document_term_matrix(max_features=15, ngram_range=(3, 3))
```

#### `get_most_common_bigrams(top_n=20)`
Get the most frequent bigrams across all characters.

```python
top_bigrams = mvc.get_most_common_bigrams(top_n=10)
# Returns: [(bigram, count), ...]
# Example: [('greek mythology', 453), ('mythical character', 60), ...]
```

#### `get_top_bigrams_per_character(character_name, top_n=5)`
Get top bigrams for a specific character.

```python
zeus_bigrams = mvc.get_top_bigrams_per_character('Zeus', top_n=5)
# Returns: [('greek god', 1), ...]
```

#### `find_similar_characters(character_name, top_n=5)`
Find characters with similar bigram distributions using cosine similarity.

```python
similar = mvc.find_similar_characters('Zeus', top_n=5)
# Returns: [(character_name, similarity_score), ...]
# Example: [('Ares', 1.000), ('Eros', 1.000), ...]
```

#### `analyze_character(character_name)`
Complete analysis of a character's bigram profile.

```python
analysis = mvc.analyze_character('Zeus')
# Returns: {
#     'name': 'Zeus',
#     'description': 'Greek god of the sky...',
#     'top_bigrams': [('greek god', 1)],
#     'similar_characters': [('Ares', 1.000), ...]
# }
```

#### `get_dtm_dataframe(top_n=50)`
Get the DTM as a pandas DataFrame.

```python
df = mvc.get_dtm_dataframe(top_n=10)
# Returns: DataFrame with characters as rows, bigrams as columns
```

#### `save_dtm_to_csv(filename="mythology_dtm.csv", top_n=100)`
Save the document-term matrix to CSV.

```python
mvc.save_dtm_to_csv("my_dtm.csv", top_n=100)
```

## Usage Examples

### Example 1: Basic Analysis

```python
from CntVector import MythologyCountVectorizer

mvc = MythologyCountVectorizer()
mvc.load_characters()
mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

# Most common bigrams
top = mvc.get_most_common_bigrams(top_n=10)
for bigram, count in top:
    print(f"{bigram}: {count}")
```

### Example 2: Character Comparison

```python
mvc = MythologyCountVectorizer()
mvc.load_characters()
mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

gods = ['Zeus', 'Poseidon', 'Hades', 'Apollo']

for god in gods:
    bigrams = mvc.get_top_bigrams_per_character(god, top_n=3)
    print(f"\n{god}:")
    for bigram, count in bigrams:
        print(f"  - '{bigram}': {count}")
```

### Example 3: Find Similar Characters

```python
mvc = MythologyCountVectorizer()
mvc.load_characters()
mvc.create_document_term_matrix(max_features=30, ngram_range=(2, 2))

similar_to_athena = mvc.find_similar_characters('Athena', top_n=5)
print("Characters similar to Athena:")
for name, score in similar_to_athena:
    print(f"  {name}: {score:.3f}")
```

### Example 4: Different N-grams

```python
mvc = MythologyCountVectorizer()
mvc.load_characters()

# Unigrams (single words)
mvc.create_document_term_matrix(max_features=15, ngram_range=(1, 1))
unigrams = mvc.get_most_common_bigrams(top_n=10)

# Trigrams (3-word phrases)
mvc.create_document_term_matrix(max_features=15, ngram_range=(3, 3))
trigrams = mvc.get_most_common_bigrams(top_n=10)
```

### Example 5: Export to CSV

```python
mvc = MythologyCountVectorizer()
mvc.load_characters()
mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

# Save first 100 characters
mvc.save_dtm_to_csv("mythology_dtm.csv", top_n=100)

# Also get as DataFrame for analysis
df = mvc.get_dtm_dataframe(top_n=100)
print(df.describe())
```

## Run the Demo

```bash
# Full demo with all features
python CntVector.py

# Run all examples
python example_cntvector.py
```

## Output Files

- **mythology_dtm.csv** - Document-term matrix exported to CSV
  - Rows: Character names
  - Columns: Bigrams
  - Values: Count of bigram in character description

## Technical Details

### CountVectorizer Configuration

```python
CountVectorizer(
    max_features=20,              # Keep top 20 features
    ngram_range=(2, 2),           # Bigrams only
    stop_words='english',         # Remove common words
    lowercase=True,               # Convert to lowercase
    min_df=2,                     # Must appear in ≥2 documents
    token_pattern=r'\b[a-zA-Z]{3,}\b'  # Words ≥3 letters
)
```

### Similarity Calculation

Uses **cosine similarity** to find characters with similar bigram distributions:

```
similarity(A, B) = (A · B) / (||A|| × ||B||)
```

Where:
- A and B are bigram count vectors
- Values range from 0 (no similarity) to 1 (identical)

## Use Cases

1. **Character Clustering** - Group characters with similar descriptions
2. **Feature Extraction** - Identify key terms in mythology
3. **Similarity Search** - Find related characters
4. **Text Analysis** - Study patterns in descriptions
5. **Data Exploration** - Understand corpus structure

## Comparison with Vector Database

| Feature | Count Vectorizer | ChromaDB Vector DB |
|---------|-----------------|-------------------|
| Method | Sparse bag-of-words | Dense embeddings |
| Similarity | Exact word matches | Semantic meaning |
| Interpretable | ✓ Yes (see exact words) | ✗ No (abstract vectors) |
| Speed | Fast | Fast |
| Storage | Efficient (sparse) | Larger (dense) |
| Best for | Term frequency analysis | Semantic search |

## Requirements

```
scikit-learn>=1.0.0
pandas>=1.5.0
numpy>=1.22.0
chromadb>=1.3.0
```

## Notes

- The DTM is **sparse** (95%+ zeros) because most bigrams don't appear in most descriptions
- **Bigrams** capture more context than unigrams but are more specific than trigrams
- **max_features=20** keeps only the top 20 most common bigrams
- Characters with **similarity=1.000** have identical bigram patterns

## Next Steps

1. Try different n-gram ranges
2. Adjust max_features for more/fewer features
3. Experiment with different min_df thresholds
4. Combine with TF-IDF weighting
5. Use for character classification

## See Also

- Main package: `mythoscifi/`
- Vector database: `query_both.py`
- Name generation: `generate_blended_names.py`
