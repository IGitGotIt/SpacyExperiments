# TF-IDF Analysis with Visualizations

## 🎉 Updated Features

The `CntVector.py` module now includes **TF-IDF (Term Frequency-Inverse Document Frequency)** analysis alongside Count Vectorization, with comprehensive visualizations!

## 📊 What's New

### 1. **TF-IDF Matrix Creation**
- Weights terms by their importance: frequent in document but rare overall
- Same 1,076 mythology characters
- Same 20 bigram features
- 95.71% sparsity (efficient storage)

### 2. **Four Visualization Types**
1. **Feature Distribution** - Compare top bigrams (Count vs TF-IDF)
2. **Character Comparison** - Side-by-side Count vs TF-IDF for characters
3. **Count Heatmap** - Character-term relationships (raw counts)
4. **TF-IDF Heatmap** - Character-term relationships (weighted scores)

## 🚀 Quick Usage

```python
from CntVector import MythologyCountVectorizer

# Initialize
mvc = MythologyCountVectorizer()
mvc.load_characters()

# Create both matrices
mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))
mvc.create_tfidf_matrix(max_features=20, ngram_range=(2, 2))

# Compare for a character
comparison = mvc.compare_count_vs_tfidf('Zeus')
print(comparison)

# Generate all visualizations
mvc.plot_feature_distribution()
mvc.plot_count_vs_tfidf(character_names=['Zeus', 'Athena', 'Poseidon'])
mvc.plot_heatmap(method='count')
mvc.plot_heatmap(method='tfidf')
```

## 📈 Generated Visualizations

### 1. **feature_distribution.png**
- **Left**: Top 15 bigrams by total count
- **Right**: Top 15 bigrams by total TF-IDF score
- **Shows**: Which terms are common vs which are distinctive

### 2. **count_vs_tfidf_comparison.png**
- **Rows**: Different characters (Zeus, Athena, Poseidon, etc.)
- **Left Column**: Count-based top bigrams
- **Right Column**: TF-IDF-based top bigrams
- **Shows**: How weighting changes important terms per character

### 3. **heatmap_count.png**
- **Heatmap**: Top 10 characters × Top 15 bigrams
- **Colors**: Blue intensity = count frequency
- **Shows**: Raw frequency patterns

### 4. **heatmap_tfidf.png**
- **Heatmap**: Top 10 characters × Top 15 bigrams
- **Colors**: Red intensity = TF-IDF score
- **Shows**: Distinctive term patterns

## 🔬 TF-IDF Explained

### What is TF-IDF?

**TF-IDF = Term Frequency × Inverse Document Frequency**

- **TF (Term Frequency)**: How often a term appears in a document
- **IDF (Inverse Document Frequency)**: How rare the term is across all documents
- **Result**: High score = term is frequent in this doc but rare overall

### Why Use TF-IDF?

| Scenario | Count Vectorizer | TF-IDF |
|----------|-----------------|---------|
| Common term | High count | Low score |
| Rare but meaningful term | Low/medium count | High score |
| Best for | Frequency analysis | Finding distinctive terms |

### Example

For Zeus's description:
- **"greek mythology"** - Appears in 453 descriptions → Low TF-IDF (common)
- **"greek god"** - Appears in 14 descriptions → Higher TF-IDF (more distinctive)

## 🎨 Visualization Methods

### `plot_feature_distribution(figsize=(12, 6))`
Compare top features across all characters.

```python
mvc.plot_feature_distribution()
# Creates: feature_distribution.png
```

**Output:**
- 2 horizontal bar charts side-by-side
- Shows top 15 bigrams for each method
- Useful for understanding corpus-level patterns

### `plot_count_vs_tfidf(character_names=None, top_n=10, figsize=(14, 8))`
Compare Count vs TF-IDF for specific characters.

```python
mvc.plot_count_vs_tfidf(
    character_names=['Zeus', 'Athena', 'Poseidon', 'Apollo', 'Aphrodite'],
    top_n=10
)
# Creates: count_vs_tfidf_comparison.png
```

**Output:**
- Row per character
- Left: Count-based terms
- Right: TF-IDF-based terms
- Shows how weighting affects term importance

### `plot_heatmap(method='count', top_chars=10, top_features=15, figsize=(12, 8))`
Visualize character-term matrix as heatmap.

```python
# Count-based heatmap
mvc.plot_heatmap(method='count', top_chars=10, top_features=15)
# Creates: heatmap_count.png

# TF-IDF-based heatmap
mvc.plot_heatmap(method='tfidf', top_chars=10, top_features=15)
# Creates: heatmap_tfidf.png
```

**Output:**
- Rows: Characters
- Columns: Bigrams
- Cell color intensity: Score magnitude
- Annotations: Exact values

## 📊 New API Methods

### `create_tfidf_matrix(max_features=20, ngram_range=(2, 2))`
Create TF-IDF matrix (similar to count matrix).

```python
mvc.create_tfidf_matrix(max_features=20, ngram_range=(2, 2))
```

### `get_tfidf_dataframe(top_n=50)`
Get TF-IDF matrix as pandas DataFrame.

```python
df = mvc.get_tfidf_dataframe(top_n=50)
print(df.head())
```

### `get_top_tfidf_per_character(character_name, top_n=5)`
Get top TF-IDF scored bigrams for a character.

```python
tfidf_terms = mvc.get_top_tfidf_per_character('Zeus', top_n=5)
# Returns: [('greek god', 1.0000), ...]
```

### `compare_count_vs_tfidf(character_name)`
Compare both methods for one character.

```python
comparison = mvc.compare_count_vs_tfidf('Zeus')
print("Count-based:", comparison['count_based'])
print("TF-IDF-based:", comparison['tfidf_based'])
```

## 📈 Results Summary

### Statistics
- **Total characters**: 1,076 Greek mythology characters
- **Count matrix**: (1076, 20) - 95.71% sparse
- **TF-IDF matrix**: (1076, 20) - 95.71% sparse
- **Features**: Top 20 bigrams
- **Visualizations**: 4 PNG files generated

### Key Findings

**Most Common Bigrams (Count):**
1. 'greek mythology' - 453 times
2. 'mythical character' - 60 times
3. 'mythical son' - 47 times

**Character Analysis:**
- **Zeus**: 'greek god' is distinctive
- **Athena**: 'ancient greek' is distinctive
- **Poseidon**: 'greek mythology' appears

## 🎯 Use Cases

### 1. Feature Comparison
```python
# See which method highlights different terms
mvc.plot_feature_distribution()
```

### 2. Character Profiling
```python
# Understand what makes each character unique
comparison = mvc.compare_count_vs_tfidf('Athena')
```

### 3. Corpus Analysis
```python
# Visualize entire dataset patterns
mvc.plot_heatmap(method='tfidf', top_chars=20, top_features=20)
```

### 4. Term Importance
```python
# Find distinctive vs common terms
count_terms = mvc.get_top_bigrams_per_character('Zeus', top_n=10)
tfidf_terms = mvc.get_top_tfidf_per_character('Zeus', top_n=10)
```

## 🔧 Customization Options

### Adjust Feature Count
```python
# More features for detailed analysis
mvc.create_document_term_matrix(max_features=50)
mvc.create_tfidf_matrix(max_features=50)
```

### Different N-grams
```python
# Try unigrams or trigrams
mvc.create_tfidf_matrix(max_features=20, ngram_range=(1, 1))  # Unigrams
mvc.create_tfidf_matrix(max_features=20, ngram_range=(3, 3))  # Trigrams
```

### Custom Visualizations
```python
# Larger heatmaps
mvc.plot_heatmap(method='tfidf', top_chars=30, top_features=30, figsize=(16, 12))

# More characters in comparison
mvc.plot_count_vs_tfidf(
    character_names=['Zeus', 'Athena', 'Poseidon', 'Apollo', 'Aphrodite', 'Ares', 'Hera'],
    top_n=15,
    figsize=(16, 20)
)
```

## 📦 Dependencies

```bash
pip install scikit-learn pandas numpy matplotlib seaborn chromadb
```

## 🚀 Run the Full Demo

```bash
# Generates all matrices and visualizations
python CntVector.py
```

**Output Files:**
- `feature_distribution.png` - Feature comparison
- `count_vs_tfidf_comparison.png` - Character comparison
- `heatmap_count.png` - Count-based heatmap
- `heatmap_tfidf.png` - TF-IDF-based heatmap
- `mythology_dtm.csv` - Count matrix as CSV

## 💡 Tips

1. **Use Count** when you want raw frequency information
2. **Use TF-IDF** when you want to find distinctive/unique terms
3. **Compare both** to understand the difference weighting makes
4. **Visualizations** help spot patterns not obvious in tables
5. **Heatmaps** are great for finding clusters of similar characters

## 🎓 Key Differences

| Aspect | Count Vectorizer | TF-IDF |
|--------|-----------------|---------|
| **Score** | Raw count | Weighted score |
| **Common terms** | High values | Downweighted |
| **Rare terms** | Low values | Upweighted |
| **Interpretation** | "How often?" | "How distinctive?" |
| **Best for** | Frequency analysis | Finding key terms |
| **Visualization** | Blue heatmap | Red heatmap |

## 📚 See Also

- **README_CNTVECTOR.md** - Full Count Vectorizer documentation
- **example_cntvector.py** - Usage examples
- **CntVector.py** - Source code

## 🎉 Summary

Your project now has:
- ✅ Count Vectorization (raw frequencies)
- ✅ TF-IDF Weighting (importance scores)
- ✅ 4 Types of visualizations
- ✅ Comparison methods
- ✅ Heatmaps for pattern analysis
- ✅ Export to PNG and CSV

All integrated in one easy-to-use class! 🚀
