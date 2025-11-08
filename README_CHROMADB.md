# ChromaDB Vector Database - Sci-Fi Robots & Greek Mythology

A local vector database containing 1,702 fictional characters for semantic search.

## Database Contents

- **626 Sci-Fi Robots** - Scraped from Wikipedia's list of fictional robots and androids
- **1,076 Greek Mythology Characters** - From Kaggle dataset (Greek Mythology Network Data)

## Files

### Setup & Storage Scripts
- `test_chroma.py` - Simple installation test
- `store_in_chroma.py` - Store only robots
- `store_both_in_chroma.py` - Store both robots AND mythology characters (recommended)

### Query Scripts
- `query_chroma.py` - Query robot database only
- `query_both.py` - Query combined database (recommended)

## Quick Start

### 1. Store Data (one-time setup)
```bash
python store_both_in_chroma.py
```
This will:
- Scrape Wikipedia for robot data
- Download Greek mythology dataset from Kaggle
- Store 1,702 characters in `./chroma_db` directory

### 2. Query the Database

**Run test queries:**
```bash
python query_both.py
```

**Custom query (all categories):**
```bash
python query_both.py "powerful warrior"
python query_both.py "Zeus"
python query_both.py "friendly robot"
```

**Filter by category:**
```bash
python query_both.py "robot: intelligent AI"
python query_both.py "mythology: goddess of wisdom"
```

**Interactive mode:**
```bash
python query_both.py
# Then choose 'y' for interactive mode
```

## Example Queries

### Mixed Search (Both Categories)
```bash
python query_both.py "powerful warrior"
```
Results: Machaon (mythology), Midas (mythology), Anticlus (mythology)...

### Mythology Only
```bash
python query_both.py "mythology: goddess of love"
```
Results: Aphrodite, Adonis, Philotes...

### Robots Only
```bash
python query_both.py "robot: companion droid"
```
Results: Companion, FemiSapien, Domestic robots...

## How It Works

1. **Vector Embeddings** - Each character's name and description is converted to a vector using ChromaDB's default embedding model (all-MiniLM-L6-v2)
2. **Semantic Search** - Queries are embedded and compared using cosine similarity
3. **Persistent Storage** - Database is saved to disk in `./chroma_db` directory
4. **Category Filtering** - Can search within specific categories (robot/mythology)

## Database Structure

Each entry contains:
- **name**: Character name
- **description**: Character description (up to 500 chars)
- **category**: Either "robot" or "mythology"
- **document**: Combined text for embedding (name + category + description)

## Similarity Scores

- **1.0** = Perfect match
- **0.3+** = High similarity
- **0.0** = Neutral
- **Negative** = Low similarity (but still closest matches)

## Requirements

- chromadb
- requests
- beautifulsoup4
- kagglehub
- pandas

Install with:
```bash
pip install chromadb requests beautifulsoup4 kagglehub pandas
```
