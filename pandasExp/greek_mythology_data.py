import kagglehub
import pandas as pd
import os


def download_dataset():
    """Download the Greek mythology dataset and return the path."""
    path = kagglehub.dataset_download("zaylaatsi/greek-mythology-network-data")
    return path


def debug_dataset_info(path):
    """Print detailed information about all CSV files in the dataset."""
    print("Path to dataset files:", path)
    print("\n" + "="*60)

    # List all files in the dataset directory
    print("\nFiles in dataset:")
    files = os.listdir(path)
    for file in files:
        print(f"  - {file}")

    print("\n" + "="*60)

    # Load and display CSV files
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(path, file)
            print(f"\nLoading: {file}")
            print("-" * 60)

            df = pd.read_csv(file_path)

            print(f"Shape: {df.shape} (rows, columns)")
            print(f"\nColumn names: {list(df.columns)}")
            print(f"\nFirst 5 rows:")
            print(df.head())
            print(f"\nData types:")
            print(df.dtypes)
            print(f"\nBasic statistics:")
            print(df.describe())
            print("\n" + "="*60)


def print_characters(path, limit=10):
    """Print the first N characters with their names and descriptions."""
    # Load the characters CSV file
    characters_file = os.path.join(path, 'characters.csv')
    df = pd.read_csv(characters_file)

    print(f"\nFirst {limit} Greek Mythology Characters:")
    print("="*80)

    for i, row in df.head(limit).iterrows():
        name = row['name']
        description = row['description'] if pd.notna(row['description']) else 'No description available'
        print(f"\n{i+1}. {name}")
        print(f"   {description}")

    print("\n" + "="*80)


if __name__ == "__main__":
    # Download dataset
    path = download_dataset()

    # Simple output: Just print first 10 characters with descriptions
    print_characters(path, limit=10)

    # Uncomment the line below to see detailed debug information
    # debug_dataset_info(path)
