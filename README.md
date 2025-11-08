# AITextProcessing - Greek Mythology & Sci-Fi Character Analysis

A comprehensive Python toolkit for analyzing Greek mythology and sci-fi robot characters using vector databases, natural language processing, and machine learning techniques.

## 🌟 Features

### 1. **Vector Database with Semantic Search**
- Store 1,702 characters (1,076 Greek mythology + 626 sci-fi robots)
- Semantic search using ChromaDB with dense embeddings
- Query by meaning, not just keywords
- Find similar characters using cosine similarity

### 2. **Unique Name Generator**
- Blend Greek mythology and sci-fi robot names
- Create pronounceable, creative combinations
- Query-guided generation for themed names
- Examples: "Cerebrolles" (Achilles + Cerebro), "Livingetus" (Admetus + Living Brain)

### 3. **Text Analysis with Count Vectorization**
- Document-term matrix with bigrams (2-word combinations)
- Sparse matrix representation (95.71% sparse)
- Character similarity based on description patterns
- Export to pandas DataFrame and CSV

### 4. **TF-IDF Weighting**
- Find distinctive terms vs common terms
- Weighted scoring for feature importance
- Identify what makes characters unique
- Compare with raw count frequencies

### 5. **Rich Visualizations**
- Count vs TF-IDF comparison plots
- Character-term heatmaps
- Feature distribution charts
- High-quality PNG exports (300 DPI)

### 6. **Installable Python Package**
- Clean package structure (`mythoscifi`)
- Install via pip in any project
- Command-line tools included
- Well-documented API

---

## 📊 Project Statistics

- **Total Characters**: 1,702
  - Greek Mythology: 1,076
  - Sci-Fi Robots: 626
- **Vector Database**: ChromaDB with all-MiniLM-L6-v2 embeddings
- **Text Features**: 20 top bigrams
- **Matrix Sparsity**: 95.71%
- **Visualizations**: 4 plot types
- **Lines of Code**: ~2,500+

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/IGitGotIt/AITextProcessing.git
cd AITextProcessing

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

### Basic Usage

#### 1. Vector Database Search

```python
from mythoscifi import CharacterDatabase

# Initialize and load database
db = CharacterDatabase()
db.initialize()

# Search for characters
results = db.search("goddess of wisdom", n_results=5)
for r in results:
    print(f"{r['name']}: {r['similarity']:.3f}")
# Output: Athena: 0.274
```

#### 2. Generate Blended Names

```python
from mythoscifi import NameGenerator

# Create generator
gen = NameGenerator(db)

# Generate themed names
names = gen.generate(query="powerful warrior", top_n=5)
for name in names:
    print(f"{name['name']} - from {name['source_myth']} + {name['source_robot']}")
```

#### 3. Count Vectorization Analysis

```python
from CntVector import MythologyCountVectorizer

# Initialize
mvc = MythologyCountVectorizer()
mvc.load_characters()

# Create document-term matrix
mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

# Get top bigrams
top = mvc.get_most_common_bigrams(top_n=10)
for bigram, count in top:
    print(f"'{bigram}': {count}")
```

#### 4. TF-IDF Analysis with Visualization

```python
# Create TF-IDF matrix
mvc.create_tfidf_matrix(max_features=20, ngram_range=(2, 2))

# Compare methods
comparison = mvc.compare_count_vs_tfidf('Zeus')
print("Count-based:", comparison['count_based'])
print("TF-IDF-based:", comparison['tfidf_based'])

# Generate visualizations
mvc.plot_feature_distribution()
mvc.plot_count_vs_tfidf(['Zeus', 'Athena', 'Poseidon'])
mvc.plot_heatmap(method='count')
mvc.plot_heatmap(method='tfidf')
```

---

## 📁 Project Structure

```
AITextProcessing/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── setup.py                       # Package installation config
│
├── mythoscifi/                    # Main package
│   ├── __init__.py               # Package exports
│   ├── database.py               # CharacterDatabase class
│   ├── name_generator.py         # NameGenerator class
│   └── cli.py                    # Command-line tools
│
├── CntVector.py                   # Count Vectorization & TF-IDF
├── example_cntvector.py           # Count vectorization examples
├── example_usage.py               # Package usage examples
├── generate_blended_names.py      # Name generation script
├── query_both.py                  # Query combined database
├── query_chroma.py                # Query robot database only
├── store_both_in_chroma.py        # Populate combined database
├── store_in_chroma.py             # Populate robot database only
├── test_chroma.py                 # ChromaDB installation test
│
├── chroma_db/                     # Vector database storage
│   └── [ChromaDB data files]
│
├── README_CHROMADB.md             # Vector database guide
├── README_CNTVECTOR.md            # Count vectorization guide
├── README_TFIDF.md                # TF-IDF analysis guide
├── README_PACKAGE.md              # Package API documentation
├── INSTALLATION_GUIDE.md          # Installation & usage guide
├── PACKAGE_SUMMARY.md             # Package overview
├── GIT_SETUP_GUIDE.md             # Git/GitHub setup help
│
├── *.png                          # Generated visualizations
└── *.csv                          # Exported data
```

---

## 🎯 Main Components

### 1. Vector Database (ChromaDB)

**Files**: `store_both_in_chroma.py`, `query_both.py`, `mythoscifi/database.py`

Store and search characters using semantic embeddings:

```bash
# Populate database (one-time setup)
python store_both_in_chroma.py

# Search characters
python query_both.py "goddess of wisdom"
python query_both.py "robot: intelligent AI"
python query_both.py "mythology: brave hero"
```

**Key Features**:
- Semantic search (finds meaning, not just keywords)
- Category filtering (mythology/robot)
- Similarity scoring
- Persistent storage

---

### 2. Name Generator

**Files**: `generate_blended_names.py`, `mythoscifi/name_generator.py`

Generate unique blended names:

```bash
# Random names
python generate_blended_names.py

# Themed names
python generate_blended_names.py "powerful warrior hero"
python generate_blended_names.py "goddess of wisdom"
python generate_blended_names.py "intelligent robot"
```

**Example Output**:
```
1. Cerebrolles ★ QUERY MATCH
   └─ Blend of: Achilles (mythology) + Cerebro's X-Men (robot)
   └─ Creativity Score: 28.5
   └─ Semantically similar to:
      1. [ROBOT] Cerebro's X-Men (similarity: -0.230)
      2. [MYTHOLOGY] Pandrosus (similarity: -0.405)
```

---

### 3. Count Vectorization

**Files**: `CntVector.py`, `example_cntvector.py`

Analyze character descriptions using bag-of-words:

```bash
# Full demo with visualizations
python CntVector.py

# Run examples
python example_cntvector.py
```

**Outputs**:
- Document-term matrix (1076 × 20)
- Top bigrams analysis
- Character similarity based on terms
- CSV export

**Top Bigrams Found**:
1. 'greek mythology' - 453 times
2. 'mythical character' - 60 times
3. 'mythical son' - 47 times

---

### 4. TF-IDF Analysis

**Files**: `CntVector.py` (integrated)

Weight terms by importance:

```python
mvc = MythologyCountVectorizer()
mvc.load_characters()
mvc.create_tfidf_matrix(max_features=20)

# Find distinctive terms
zeus_tfidf = mvc.get_top_tfidf_per_character('Zeus', top_n=5)
```

**Visualizations Generated**:
- `feature_distribution.png` - Count vs TF-IDF comparison
- `count_vs_tfidf_comparison.png` - Character-level comparison
- `heatmap_count.png` - Count-based heatmap
- `heatmap_tfidf.png` - TF-IDF-based heatmap

---

### 5. Python Package (mythoscifi)

**Files**: `mythoscifi/`, `setup.py`

Installable package for use in other projects:

```bash
# Install
pip install -e .

# Use in any Python script
from mythoscifi import CharacterDatabase, NameGenerator

db = CharacterDatabase().initialize()
gen = NameGenerator(db)
names = gen.generate(query="space explorer", top_n=5)
```

**Command-line tools**:
```bash
mythoscifi-populate          # Populate database
mythoscifi-search "Zeus"     # Search characters
mythoscifi-generate "hero"   # Generate names
```

---

## 📚 Documentation

| File | Description |
|------|-------------|
| **README.md** | This file - project overview |
| **README_CHROMADB.md** | Vector database usage guide |
| **README_CNTVECTOR.md** | Count vectorization guide |
| **README_TFIDF.md** | TF-IDF analysis guide |
| **README_PACKAGE.md** | Package API reference |
| **INSTALLATION_GUIDE.md** | How to use in other projects |
| **PACKAGE_SUMMARY.md** | Quick package overview |
| **GIT_SETUP_GUIDE.md** | Git/GitHub authentication help |

---

## 🔧 Technologies Used

### Core Libraries
- **ChromaDB** (1.3.4) - Vector database
- **scikit-learn** (1.0+) - Count vectorization, TF-IDF
- **pandas** (1.5+) - Data manipulation
- **numpy** (1.22+) - Numerical operations

### Data Collection
- **requests** (2.28+) - HTTP requests
- **beautifulsoup4** (4.11+) - Web scraping
- **kagglehub** (0.1+) - Dataset download

### Visualization
- **matplotlib** (3.9+) - Plotting
- **seaborn** (0.13+) - Statistical visualizations

### NLP & Embeddings
- **spaCy** (3.0+) - NLP toolkit (optional)
- Built-in embeddings from ChromaDB (all-MiniLM-L6-v2)

---

## 📊 Data Sources

1. **Greek Mythology Characters** (1,076)
   - Source: [Kaggle - Greek Mythology Network Data](https://www.kaggle.com/datasets/zaylaatsi/greek-mythology-network-data)
   - License: Public Domain
   - Fields: name, description

2. **Sci-Fi Robots & Androids** (626)
   - Source: [Wikipedia - List of Fictional Robots and Androids](https://en.wikipedia.org/wiki/List_of_fictional_robots_and_androids)
   - License: CC BY-SA
   - Fields: name, description, source

---

## 💡 Use Cases

### 1. **Research & Analysis**
- Study patterns in mythology descriptions
- Analyze robot character archetypes
- Compare semantic vs frequency-based methods

### 2. **Creative Writing**
- Generate unique character names
- Find inspiration from similar characters
- Blend mythology with sci-fi themes

### 3. **Game Development**
- Create NPC names
- Generate character backstories
- Build character databases

### 4. **Educational**
- Learn NLP techniques
- Understand vector databases
- Practice text analysis methods

### 5. **Data Science**
- Compare ML/NLP approaches
- Visualize high-dimensional data
- Build recommendation systems

---

## 🎨 Example Outputs

### Blended Names
```
Cerebrolles (Achilles + Cerebro's X-Men)
Livingetus (Admetus + Living Brain)
Aegix-men (Aegipan + X-Men)
Agesifoster (Agesilaus I + Tory Foster)
```

### Search Results
```
Query: "goddess of wisdom"
1. Athena: 0.274
2. Pheme: 0.061
3. Tyche: 0.059
```

### Top Bigrams
```
1. 'greek mythology' - 453 times
2. 'mythical character' - 60 times
3. 'mythical son' - 47 times
```

---

## 🚀 Advanced Usage

### Custom Database Path
```python
db = CharacterDatabase(persist_directory="/custom/path/chroma_db")
db.initialize()
```

### Different N-grams
```python
# Unigrams (single words)
mvc.create_document_term_matrix(max_features=30, ngram_range=(1, 1))

# Trigrams (3-word phrases)
mvc.create_document_term_matrix(max_features=15, ngram_range=(3, 3))
```

### Custom Visualizations
```python
# Larger heatmap
mvc.plot_heatmap(method='tfidf', top_chars=30, top_features=30, figsize=(16, 12))

# More characters in comparison
mvc.plot_count_vs_tfidf(
    character_names=['Zeus', 'Athena', 'Poseidon', 'Apollo', 'Aphrodite', 'Ares'],
    top_n=15
)
```

---

## 🧪 Testing

```bash
# Test ChromaDB installation
python test_chroma.py

# Test package usage
python example_usage.py

# Test count vectorization
python example_cntvector.py
```

---

## 📈 Performance

| Component | Size | Speed |
|-----------|------|-------|
| Vector DB | 1,702 docs | ~100ms query |
| Count Matrix | 1,076 × 20 | ~50ms creation |
| TF-IDF Matrix | 1,076 × 20 | ~50ms creation |
| Name Generation | 100 samples | ~2s |
| Visualizations | 4 plots | ~5s total |

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add more data sources
- [ ] Implement additional NLP techniques
- [ ] Expand visualization options
- [ ] Add more name blending algorithms
- [ ] Create web interface
- [ ] Add unit tests
- [ ] Improve documentation

---

## 📝 License

MIT License - see LICENSE file for details

---

## 👤 Author

**Your Name**
- GitHub: [@IGitGotIt](https://github.com/IGitGotIt)

---

## 🙏 Acknowledgments

- **ChromaDB** - Vector database framework
- **scikit-learn** - Machine learning library
- **Kaggle** - Greek mythology dataset
- **Wikipedia** - Sci-fi robot data
- **Claude Code** - Development assistance

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/IGitGotIt/AITextProcessing/issues)
- **Documentation**: See README_*.md files
- **Examples**: Check example_*.py files

---

## 🎓 Learning Resources

### Tutorials Included
1. Vector database basics → `README_CHROMADB.md`
2. Count vectorization → `README_CNTVECTOR.md`
3. TF-IDF analysis → `README_TFIDF.md`
4. Package usage → `README_PACKAGE.md`
5. Installation → `INSTALLATION_GUIDE.md`

### Concepts Covered
- Vector embeddings
- Semantic search
- Sparse matrices
- TF-IDF weighting
- Cosine similarity
- N-gram analysis
- Data visualization
- Python packaging

---

## 🔮 Future Enhancements

- [ ] Web interface with Flask/FastAPI
- [ ] More visualization types
- [ ] Additional text analysis methods
- [ ] Character classification
- [ ] Relationship mapping
- [ ] Interactive dashboards
- [ ] API endpoints
- [ ] Docker containerization

---

## ⚡ Quick Commands Cheat Sheet

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Populate database
python store_both_in_chroma.py

# Search
python query_both.py "Zeus"

# Generate names
python generate_blended_names.py "warrior"

# Analyze text
python CntVector.py

# Install package
pip install -e .
```

---

## 📊 Project Metrics

- **Files**: 30+ Python/Markdown files
- **Functions**: 50+ methods
- **Documentation**: 8 comprehensive guides
- **Visualizations**: 4 plot types
- **Data Points**: 1,702 characters
- **Features**: 20 bigrams
- **Matrix Size**: 1,076 × 20

---

**Built with ❤️ using Python, ChromaDB, scikit-learn, and Claude Code**

🚀 **Star this repo if you find it useful!** ⭐
