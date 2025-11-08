# MythoSciFi Package - Installation & Usage Guide

## 📦 Package Structure

Your project has been packaged as **mythoscifi** with the following structure:

```
SpacyExperiments/
├── mythoscifi/                  # Main package
│   ├── __init__.py             # Package exports
│   ├── database.py             # Database management
│   ├── name_generator.py       # Name generation
│   └── cli.py                  # Command-line tools
├── setup.py                    # Installation config
├── requirements.txt            # Dependencies
├── README_PACKAGE.md           # Package documentation
├── example_usage.py            # Usage examples
└── chroma_db/                  # Vector database (data)
```

## 🚀 Installation Options

### Option 1: Install in Current Environment (Development Mode)

From within `/Users/jaideep/Documents/AIProjects/SpacyExperiments`:

```bash
pip install -e .
```

**Pros:**
- ✓ Changes to code are immediately reflected
- ✓ Good for development and testing
- ✓ Package can be imported from anywhere

**Cons:**
- ✗ Only works in current Python environment

### Option 2: Install in Another Project

From **any other folder**:

```bash
# Install from local directory
pip install /Users/jaideep/Documents/AIProjects/SpacyExperiments

# Or if you want editable mode
pip install -e /Users/jaideep/Documents/AIProjects/SpacyExperiments
```

**Example:**
```bash
# Create new project
mkdir ~/my_new_project
cd ~/my_new_project

# Install mythoscifi
pip install /Users/jaideep/Documents/AIProjects/SpacyExperiments

# Use it!
python -c "from mythoscifi import CharacterDatabase; print('Works!')"
```

### Option 3: Build and Distribute

Create a distributable package:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# This creates:
# - dist/mythoscifi-0.1.0.tar.gz
# - dist/mythoscifi-0.1.0-py3-none-any.whl

# Install from wheel file
pip install dist/mythoscifi-0.1.0-py3-none-any.whl

# Or share the wheel file with others
```

### Option 4: Upload to PyPI (Public)

```bash
# Build first
python -m build

# Upload to PyPI (requires account)
python -m twine upload dist/*

# Then anyone can install:
pip install mythoscifi
```

## 📝 Usage in Another Project

### Method 1: Using the Library

```python
# my_project.py
from mythoscifi import CharacterDatabase, NameGenerator

# Initialize (point to your existing database)
db = CharacterDatabase(
    persist_directory="/Users/jaideep/Documents/AIProjects/SpacyExperiments/chroma_db"
)
db.initialize()

# Search
results = db.search("goddess of wisdom", n_results=5)
for r in results:
    print(f"{r['name']}: {r['similarity']:.3f}")

# Generate names
gen = NameGenerator(db)
names = gen.generate(query="brave warrior", top_n=5)

for name in names:
    print(name['name'])
```

### Method 2: Create New Database in Your Project

```python
from mythoscifi import CharacterDatabase

# Create database in your project folder
db = CharacterDatabase(persist_directory="./my_chroma_db")
db.initialize()

# Populate with data (first time only - takes a few minutes)
db.populate(fetch_robots=True, fetch_mythology=True)

# Now use it
results = db.search("hero", n_results=10)
```

### Method 3: Using Command Line Tools

After installing with `pip install -e .`:

```bash
# Populate database (first time)
mythoscifi-populate

# Search
mythoscifi-search "goddess of love"

# Generate names
mythoscifi-generate "powerful warrior"
```

## 🔧 Common Use Cases

### Use Case 1: Flask Web API

```python
# app.py
from flask import Flask, jsonify, request
from mythoscifi import CharacterDatabase, NameGenerator

app = Flask(__name__)

# Initialize once at startup
db = CharacterDatabase(persist_directory="../SpacyExperiments/chroma_db")
db.initialize()
generator = NameGenerator(db)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    results = db.search(query, n_results=10)
    return jsonify(results)

@app.route('/api/generate')
def api_generate():
    query = request.args.get('q', None)
    names = generator.generate(query=query, top_n=5)
    return jsonify(names)

if __name__ == '__main__':
    app.run(port=5000)
```

Test:
```bash
# Start server
python app.py

# Test in browser or curl
curl "http://localhost:5000/api/search?q=Zeus"
curl "http://localhost:5000/api/generate?q=warrior"
```

### Use Case 2: Game Character Generator

```python
# game_characters.py
from mythoscifi import CharacterDatabase, NameGenerator
import random

class RPGCharacterGenerator:
    def __init__(self, db_path):
        self.db = CharacterDatabase(persist_directory=db_path)
        self.db.initialize()
        self.gen = NameGenerator(self.db)

    def create_character(self, character_class):
        queries = {
            'warrior': 'strong brave fighter',
            'mage': 'wise magical wizard',
            'rogue': 'cunning stealth thief',
            'cleric': 'holy divine healer'
        }

        query = queries.get(character_class, 'hero')
        names = self.gen.generate(query=query, top_n=1)

        return {
            'name': names[0]['name'],
            'class': character_class,
            'level': 1,
            'lore': f"Born from the legends of {names[0]['source_myth']} "
                   f"and powered by {names[0]['source_robot']}"
        }

# Usage
gen = RPGCharacterGenerator("./chroma_db")
warrior = gen.create_character('warrior')
print(f"Name: {warrior['name']}")
print(f"Lore: {warrior['lore']}")
```

### Use Case 3: Batch Name Generation Script

```python
# batch_generate.py
from mythoscifi import CharacterDatabase, NameGenerator
import json

def generate_batch(theme, count=50):
    db = CharacterDatabase()
    db.initialize()
    gen = NameGenerator(db)

    all_names = []
    for _ in range(count // 5):  # Generate in batches
        names = gen.generate(query=theme, top_n=5)
        all_names.extend(names)

    # Save to file
    output = {
        'theme': theme,
        'count': len(all_names),
        'names': [
            {
                'name': n['name'],
                'from': f"{n['source_myth']} + {n['source_robot']}",
                'score': n['creativity_score']
            }
            for n in all_names
        ]
    }

    filename = f"names_{theme.replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Generated {len(all_names)} names saved to {filename}")

# Generate themed name sets
generate_batch("space explorer", count=50)
generate_batch("ancient god", count=50)
```

## 📊 Database Management

### Check Database Stats

```python
from mythoscifi import CharacterDatabase

db = CharacterDatabase()
db.initialize()

stats = db.get_stats()
print(f"Total: {stats['total']}")
print(f"Robots: {stats['robots']}")
print(f"Mythology: {stats['mythology']}")
```

### Search with Filters

```python
# Search only mythology
results = db.search("hero", n_results=10, filter_category="mythology")

# Search only robots
results = db.search("AI", n_results=10, filter_category="robot")
```

### Get Random Characters

```python
# Get random mythology characters
myths = db.get_random_characters(category="mythology", limit=50)

# Get random robots
robots = db.get_random_characters(category="robot", limit=50)
```

## 🐛 Troubleshooting

### Package not found after installation

```bash
# Check if installed
pip list | grep mythoscifi

# Reinstall
pip uninstall mythoscifi
pip install -e /path/to/SpacyExperiments
```

### Database not found

Make sure you point to the correct database path:

```python
# Use absolute path
db = CharacterDatabase(
    persist_directory="/Users/jaideep/Documents/AIProjects/SpacyExperiments/chroma_db"
)

# Or create new database
db = CharacterDatabase(persist_directory="./my_db")
db.populate()  # This will download and populate
```

### Import errors

```bash
# Make sure dependencies are installed
pip install -r /Users/jaideep/Documents/AIProjects/SpacyExperiments/requirements.txt
```

## 📦 Distribution Checklist

To share your package with others:

1. **Update metadata in setup.py**
   - Change author name and email
   - Add proper description
   - Update URL

2. **Build the package**
   ```bash
   python -m build
   ```

3. **Test the build**
   ```bash
   pip install dist/mythoscifi-0.1.0-py3-none-any.whl
   ```

4. **Share**
   - Send the `.whl` file to others
   - Or upload to GitHub and pip install from GitHub
   - Or publish to PyPI

## 🎓 Next Steps

1. **Try the examples** in `example_usage.py`
2. **Read the full API** in `README_PACKAGE.md`
3. **Build something cool** with the package!

## 📫 Support

For issues or questions, check:
- Package documentation: `README_PACKAGE.md`
- Example usage: `example_usage.py`
- Original scripts in the project root
