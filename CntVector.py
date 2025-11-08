"""
Count Vectorization and TF-IDF for Mythological Characters using scikit-learn.

This module creates a document-term matrix from mythological character descriptions
using CountVectorizer and TfidfVectorizer with bigrams (2-word combinations).
"""

import chromadb
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class MythologyCountVectorizer:
    """Count vectorization for mythology character descriptions."""

    def __init__(self, persist_directory="./chroma_db"):
        """
        Initialize the vectorizer.

        Args:
            persist_directory: Path to ChromaDB database
        """
        self.persist_directory = persist_directory
        self.db_client = None
        self.collection = None
        self.vectorizer = None
        self.tfidf_vectorizer = None
        self.dtm = None  # Document-Term Matrix (Count)
        self.tfidf_matrix = None  # TF-IDF Matrix
        self.characters = []
        self.feature_names = []
        self.tfidf_feature_names = []

    def load_characters(self):
        """Load mythology characters from ChromaDB."""
        print("Loading mythology characters from ChromaDB...")
        self.db_client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.db_client.get_collection(name="characters")

        # Get only mythology characters
        results = self.collection.get(
            where={"category": "mythology"},
            limit=10000  # Get all mythology characters
        )

        self.characters = []
        for metadata in results['metadatas']:
            self.characters.append({
                'name': metadata['name'],
                'description': metadata['description'],
                'category': metadata['category']
            })

        print(f"✓ Loaded {len(self.characters)} mythology characters")
        return self

    def create_document_term_matrix(self, max_features=20, ngram_range=(2, 2)):
        """
        Create a document-term matrix using CountVectorizer with bigrams.

        Args:
            max_features: Maximum number of features (columns) to keep
            ngram_range: Range of n-grams (default (2,2) for bigrams only)

        Returns:
            self for method chaining
        """
        if not self.characters:
            raise ValueError("No characters loaded. Call load_characters() first.")

        print(f"\nCreating document-term matrix with {max_features} features...")
        print(f"Using n-gram range: {ngram_range}")

        # Extract descriptions as documents
        documents = [char['description'] for char in self.characters]

        # Create CountVectorizer with bigrams
        self.vectorizer = CountVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,  # (2,2) for bigrams
            stop_words='english',     # Remove common English words
            lowercase=True,
            min_df=2,                 # Must appear in at least 2 documents
            token_pattern=r'\b[a-zA-Z]{3,}\b'  # Words with at least 3 letters
        )

        # Fit and transform
        self.dtm = self.vectorizer.fit_transform(documents)
        self.feature_names = self.vectorizer.get_feature_names_out()

        print(f"✓ Document-Term Matrix shape: {self.dtm.shape}")
        print(f"  - Documents (characters): {self.dtm.shape[0]}")
        print(f"  - Features (bigrams): {self.dtm.shape[1]}")

        return self

    def get_dtm_dataframe(self, top_n=50):
        """
        Get the document-term matrix as a pandas DataFrame.

        Args:
            top_n: Number of top characters to include (default 50)

        Returns:
            pandas DataFrame with characters as rows and bigrams as columns
        """
        if self.dtm is None:
            raise ValueError("DTM not created. Call create_document_term_matrix() first.")

        # Convert sparse matrix to dense for top_n characters
        dtm_dense = self.dtm[:top_n].toarray()

        # Create DataFrame
        df = pd.DataFrame(
            dtm_dense,
            columns=self.feature_names,
            index=[char['name'] for char in self.characters[:top_n]]
        )

        return df

    def get_top_bigrams_per_character(self, character_name, top_n=5):
        """
        Get the top bigrams for a specific character.

        Args:
            character_name: Name of the character
            top_n: Number of top bigrams to return

        Returns:
            List of tuples (bigram, count)
        """
        # Find character index
        char_idx = None
        for i, char in enumerate(self.characters):
            if char['name'] == character_name:
                char_idx = i
                break

        if char_idx is None:
            return []

        # Get counts for this character
        char_vector = self.dtm[char_idx].toarray().flatten()

        # Get top bigrams
        top_indices = char_vector.argsort()[-top_n:][::-1]
        top_bigrams = [(self.feature_names[i], char_vector[i])
                       for i in top_indices if char_vector[i] > 0]

        return top_bigrams

    def get_most_common_bigrams(self, top_n=20):
        """
        Get the most common bigrams across all mythology characters.

        Args:
            top_n: Number of top bigrams to return

        Returns:
            List of tuples (bigram, total_count)
        """
        if self.dtm is None:
            raise ValueError("DTM not created. Call create_document_term_matrix() first.")

        # Sum across all documents
        bigram_counts = np.asarray(self.dtm.sum(axis=0)).flatten()

        # Get top indices
        top_indices = bigram_counts.argsort()[-top_n:][::-1]

        top_bigrams = [(self.feature_names[i], int(bigram_counts[i]))
                       for i in top_indices]

        return top_bigrams

    def find_similar_characters(self, character_name, top_n=5):
        """
        Find characters with similar bigram distributions using cosine similarity.

        Args:
            character_name: Name of the character
            top_n: Number of similar characters to return

        Returns:
            List of tuples (character_name, similarity_score)
        """
        from sklearn.metrics.pairwise import cosine_similarity

        # Find character index
        char_idx = None
        for i, char in enumerate(self.characters):
            if char['name'] == character_name:
                char_idx = i
                break

        if char_idx is None:
            return []

        # Calculate cosine similarity
        char_vector = self.dtm[char_idx]
        similarities = cosine_similarity(char_vector, self.dtm).flatten()

        # Get top similar (excluding the character itself)
        top_indices = similarities.argsort()[-top_n-1:][::-1]
        similar_chars = []

        for idx in top_indices:
            if idx != char_idx:
                similar_chars.append((
                    self.characters[idx]['name'],
                    similarities[idx]
                ))

        return similar_chars[:top_n]

    def analyze_character(self, character_name):
        """
        Complete analysis of a character's bigram profile.

        Args:
            character_name: Name of the character

        Returns:
            Dictionary with analysis results
        """
        # Find character
        char_data = None
        for char in self.characters:
            if char['name'] == character_name:
                char_data = char
                break

        if not char_data:
            return {"error": f"Character '{character_name}' not found"}

        top_bigrams = self.get_top_bigrams_per_character(character_name, top_n=5)
        similar_chars = self.find_similar_characters(character_name, top_n=5)

        return {
            'name': character_name,
            'description': char_data['description'][:200],
            'top_bigrams': top_bigrams,
            'similar_characters': similar_chars
        }

    def save_dtm_to_csv(self, filename="mythology_dtm.csv", top_n=100):
        """
        Save the document-term matrix to a CSV file.

        Args:
            filename: Output filename
            top_n: Number of characters to include
        """
        df = self.get_dtm_dataframe(top_n=top_n)
        df.to_csv(filename)
        print(f"\n✓ Saved DTM to {filename}")
        print(f"  Shape: {df.shape}")

    def create_tfidf_matrix(self, max_features=20, ngram_range=(2, 2)):
        """
        Create a TF-IDF matrix using TfidfVectorizer.

        TF-IDF (Term Frequency-Inverse Document Frequency) gives higher weight to
        terms that are frequent in a document but rare across all documents.

        Args:
            max_features: Maximum number of features (columns) to keep
            ngram_range: Range of n-grams (default (2,2) for bigrams only)

        Returns:
            self for method chaining
        """
        if not self.characters:
            raise ValueError("No characters loaded. Call load_characters() first.")

        print(f"\nCreating TF-IDF matrix with {max_features} features...")
        print(f"Using n-gram range: {ngram_range}")

        # Extract descriptions as documents
        documents = [char['description'] for char in self.characters]

        # Create TfidfVectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            stop_words='english',
            lowercase=True,
            min_df=2,
            token_pattern=r'\b[a-zA-Z]{3,}\b'
        )

        # Fit and transform
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
        self.tfidf_feature_names = self.tfidf_vectorizer.get_feature_names_out()

        print(f"✓ TF-IDF Matrix shape: {self.tfidf_matrix.shape}")
        print(f"  - Documents (characters): {self.tfidf_matrix.shape[0]}")
        print(f"  - Features (bigrams): {self.tfidf_matrix.shape[1]}")

        return self

    def get_tfidf_dataframe(self, top_n=50):
        """
        Get the TF-IDF matrix as a pandas DataFrame.

        Args:
            top_n: Number of top characters to include

        Returns:
            pandas DataFrame with characters as rows and bigrams as columns
        """
        if self.tfidf_matrix is None:
            raise ValueError("TF-IDF matrix not created. Call create_tfidf_matrix() first.")

        # Convert sparse matrix to dense for top_n characters
        tfidf_dense = self.tfidf_matrix[:top_n].toarray()

        # Create DataFrame
        df = pd.DataFrame(
            tfidf_dense,
            columns=self.tfidf_feature_names,
            index=[char['name'] for char in self.characters[:top_n]]
        )

        return df

    def get_top_tfidf_per_character(self, character_name, top_n=5):
        """
        Get the top TF-IDF scored bigrams for a specific character.

        Args:
            character_name: Name of the character
            top_n: Number of top bigrams to return

        Returns:
            List of tuples (bigram, tfidf_score)
        """
        # Find character index
        char_idx = None
        for i, char in enumerate(self.characters):
            if char['name'] == character_name:
                char_idx = i
                break

        if char_idx is None:
            return []

        # Get TF-IDF scores for this character
        char_vector = self.tfidf_matrix[char_idx].toarray().flatten()

        # Get top bigrams
        top_indices = char_vector.argsort()[-top_n:][::-1]
        top_bigrams = [(self.tfidf_feature_names[i], char_vector[i])
                       for i in top_indices if char_vector[i] > 0]

        return top_bigrams

    def compare_count_vs_tfidf(self, character_name):
        """
        Compare Count and TF-IDF scores for a character.

        Args:
            character_name: Name of the character

        Returns:
            Dictionary with comparison data
        """
        if self.dtm is None or self.tfidf_matrix is None:
            raise ValueError("Both matrices must be created first.")

        count_bigrams = self.get_top_bigrams_per_character(character_name, top_n=10)
        tfidf_bigrams = self.get_top_tfidf_per_character(character_name, top_n=10)

        return {
            'character': character_name,
            'count_based': count_bigrams,
            'tfidf_based': tfidf_bigrams
        }

    def plot_count_vs_tfidf(self, character_names=None, top_n=10, figsize=(14, 8)):
        """
        Plot comparison of Count vs TF-IDF for selected characters.

        Args:
            character_names: List of character names (default: top 5 gods)
            top_n: Number of top terms to show per character
            figsize: Figure size tuple
        """
        if self.dtm is None or self.tfidf_matrix is None:
            raise ValueError("Both matrices must be created first.")

        if character_names is None:
            character_names = ['Zeus', 'Athena', 'Poseidon', 'Apollo', 'Aphrodite']

        # Filter to characters that exist
        valid_chars = []
        for name in character_names:
            if any(c['name'] == name for c in self.characters):
                valid_chars.append(name)

        if not valid_chars:
            print("No valid characters found for plotting")
            return

        fig, axes = plt.subplots(len(valid_chars), 2, figsize=figsize)
        if len(valid_chars) == 1:
            axes = axes.reshape(1, -1)

        for i, char_name in enumerate(valid_chars):
            comparison = self.compare_count_vs_tfidf(char_name)

            # Count-based (left subplot)
            count_data = comparison['count_based'][:top_n]
            if count_data:
                terms = [t[0] for t in count_data]
                values = [t[1] for t in count_data]

                axes[i, 0].barh(range(len(terms)), values, color='steelblue')
                axes[i, 0].set_yticks(range(len(terms)))
                axes[i, 0].set_yticklabels(terms)
                axes[i, 0].set_xlabel('Count')
                axes[i, 0].set_title(f'{char_name} - Count Vectorizer')
                axes[i, 0].invert_yaxis()

            # TF-IDF-based (right subplot)
            tfidf_data = comparison['tfidf_based'][:top_n]
            if tfidf_data:
                terms = [t[0] for t in tfidf_data]
                values = [t[1] for t in tfidf_data]

                axes[i, 1].barh(range(len(terms)), values, color='coral')
                axes[i, 1].set_yticks(range(len(terms)))
                axes[i, 1].set_yticklabels(terms)
                axes[i, 1].set_xlabel('TF-IDF Score')
                axes[i, 1].set_title(f'{char_name} - TF-IDF')
                axes[i, 1].invert_yaxis()

        plt.tight_layout()
        plt.savefig('count_vs_tfidf_comparison.png', dpi=300, bbox_inches='tight')
        print("\n✓ Saved plot to 'count_vs_tfidf_comparison.png'")
        plt.show()

    def plot_feature_distribution(self, figsize=(12, 6)):
        """
        Plot the distribution of top features for Count and TF-IDF.

        Args:
            figsize: Figure size tuple
        """
        if self.dtm is None or self.tfidf_matrix is None:
            raise ValueError("Both matrices must be created first.")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Count distribution
        count_sums = np.asarray(self.dtm.sum(axis=0)).flatten()
        top_count_indices = count_sums.argsort()[-15:][::-1]

        features = [self.feature_names[i] for i in top_count_indices]
        values = [count_sums[i] for i in top_count_indices]

        ax1.barh(range(len(features)), values, color='steelblue')
        ax1.set_yticks(range(len(features)))
        ax1.set_yticklabels(features, fontsize=9)
        ax1.set_xlabel('Total Count', fontsize=10)
        ax1.set_title('Top 15 Bigrams - Count Vectorizer', fontsize=12, fontweight='bold')
        ax1.invert_yaxis()

        # TF-IDF distribution
        tfidf_sums = np.asarray(self.tfidf_matrix.sum(axis=0)).flatten()
        top_tfidf_indices = tfidf_sums.argsort()[-15:][::-1]

        features = [self.tfidf_feature_names[i] for i in top_tfidf_indices]
        values = [tfidf_sums[i] for i in top_tfidf_indices]

        ax2.barh(range(len(features)), values, color='coral')
        ax2.set_yticks(range(len(features)))
        ax2.set_yticklabels(features, fontsize=9)
        ax2.set_xlabel('Total TF-IDF Score', fontsize=10)
        ax2.set_title('Top 15 Bigrams - TF-IDF', fontsize=12, fontweight='bold')
        ax2.invert_yaxis()

        plt.tight_layout()
        plt.savefig('feature_distribution.png', dpi=300, bbox_inches='tight')
        print("\n✓ Saved plot to 'feature_distribution.png'")
        plt.show()

    def plot_heatmap(self, method='count', top_chars=10, top_features=15, figsize=(12, 8)):
        """
        Plot a heatmap of character-term relationships.

        Args:
            method: 'count' or 'tfidf'
            top_chars: Number of top characters to include
            top_features: Number of top features to show
            figsize: Figure size tuple
        """
        if method == 'count':
            if self.dtm is None:
                raise ValueError("Count matrix not created.")
            df = self.get_dtm_dataframe(top_n=top_chars)
            title = 'Count Vectorizer Heatmap'
            cmap = 'Blues'
        else:
            if self.tfidf_matrix is None:
                raise ValueError("TF-IDF matrix not created.")
            df = self.get_tfidf_dataframe(top_n=top_chars)
            title = 'TF-IDF Heatmap'
            cmap = 'Reds'

        # Select top features by total score
        top_cols = df.sum(axis=0).nlargest(top_features).index
        df_subset = df[top_cols]

        plt.figure(figsize=figsize)
        sns.heatmap(df_subset, annot=True, fmt='.2f', cmap=cmap, cbar_kws={'label': 'Score'})
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Bigrams', fontsize=11)
        plt.ylabel('Characters', fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        filename = f'heatmap_{method}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✓ Saved heatmap to '{filename}'")
        plt.show()


def main():
    """Demonstration of count vectorization and TF-IDF for mythology characters."""

    print("="*80)
    print("COUNT VECTORIZATION & TF-IDF FOR MYTHOLOGY CHARACTERS")
    print("="*80)

    # Initialize and load
    mvc = MythologyCountVectorizer()
    mvc.load_characters()

    # Create document-term matrix with bigrams (20 columns)
    mvc.create_document_term_matrix(max_features=20, ngram_range=(2, 2))

    # Create TF-IDF matrix
    mvc.create_tfidf_matrix(max_features=20, ngram_range=(2, 2))

    # Display most common bigrams (Count)
    print("\n" + "="*80)
    print("TOP 20 MOST COMMON BIGRAMS - COUNT VECTORIZER")
    print("="*80)

    top_bigrams = mvc.get_most_common_bigrams(top_n=20)
    for i, (bigram, count) in enumerate(top_bigrams, 1):
        print(f"{i:2d}. '{bigram}' - appears {count} times")

    # Show document-term matrix for first 10 characters
    print("\n" + "="*80)
    print("DOCUMENT-TERM MATRIX (First 10 Characters)")
    print("="*80)

    dtm_df = mvc.get_dtm_dataframe(top_n=10)
    print(dtm_df.to_string())

    # Compare Count vs TF-IDF for specific characters
    print("\n" + "="*80)
    print("COUNT VS TF-IDF COMPARISON")
    print("="*80)

    example_chars = ['Zeus', 'Athena', 'Poseidon']

    for char_name in example_chars:
        comparison = mvc.compare_count_vs_tfidf(char_name)

        print(f"\n{char_name}:")
        print(f"  Count-based top bigrams:")
        for bigram, count in comparison['count_based'][:5]:
            print(f"    - '{bigram}': {count}")

        print(f"  TF-IDF-based top bigrams:")
        for bigram, score in comparison['tfidf_based'][:5]:
            print(f"    - '{bigram}': {score:.4f}")

    # Show statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Total characters analyzed: {len(mvc.characters)}")
    print(f"Count Matrix shape: {mvc.dtm.shape}")
    print(f"TF-IDF Matrix shape: {mvc.tfidf_matrix.shape}")
    print(f"Count sparsity: {(1.0 - (mvc.dtm.nnz / (mvc.dtm.shape[0] * mvc.dtm.shape[1]))) * 100:.2f}%")
    print(f"TF-IDF sparsity: {(1.0 - (mvc.tfidf_matrix.nnz / (mvc.tfidf_matrix.shape[0] * mvc.tfidf_matrix.shape[1]))) * 100:.2f}%")

    # Generate visualizations
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80)

    # Plot feature distributions
    print("\n1. Feature Distribution Comparison...")
    mvc.plot_feature_distribution()

    # Plot Count vs TF-IDF comparison for characters
    print("\n2. Character-based Count vs TF-IDF Comparison...")
    mvc.plot_count_vs_tfidf(character_names=['Zeus', 'Athena', 'Poseidon'])

    # Plot heatmaps
    print("\n3. Count Vectorizer Heatmap...")
    mvc.plot_heatmap(method='count', top_chars=10, top_features=15)

    print("\n4. TF-IDF Heatmap...")
    mvc.plot_heatmap(method='tfidf', top_chars=10, top_features=15)

    # Save DTM to CSV
    print("\n" + "="*80)
    print("SAVING DATA")
    print("="*80)
    mvc.save_dtm_to_csv("mythology_dtm.csv", top_n=50)

    print("\n" + "="*80)
    print("COMPLETE! Check the generated PNG files for visualizations.")
    print("="*80)


if __name__ == "__main__":
    main()
