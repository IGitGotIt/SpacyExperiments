import spacy
from collections import Counter
import os
import requests
from bs4 import BeautifulSoup


def fetch_wikipedia_robots():
    """Fetch the list of fictional robots and androids from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_fictional_robots_and_androids"

    print(f"Fetching data from: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract robot names from all list items and tables
    robots = []

    # Try to find robot names in list format (often in alphabetical sections)
    # Look for headings like "A", "B", "C" and lists under them
    content = soup.find('div', class_='mw-parser-output')

    if content:
        current_section = None
        for element in content.find_all(['h2', 'h3', 'ul', 'table']):
            if element.name in ['h2', 'h3']:
                # Track current section
                current_section = element.get_text(strip=True)

            elif element.name == 'ul':
                # Extract from unordered lists
                for li in element.find_all('li', recursive=False):
                    text = li.get_text(separator=' ', strip=True)
                    # Try to extract robot name (usually before first dash or parenthesis)
                    if ' – ' in text:
                        name, desc = text.split(' – ', 1)
                    elif ' - ' in text:
                        name, desc = text.split(' - ', 1)
                    else:
                        name = text.split('(')[0].strip() if '(' in text else text
                        desc = text

                    if name and len(name) > 1:
                        robots.append({
                            'name': name,
                            'description': desc[:200]  # Limit description length
                        })

    return robots


def debug_robot_info(robots, soup):
    """Print detailed information about the scraped data."""
    print("\n" + "="*80)
    print("DEBUG: Detailed Scraping Analysis")
    print("="*80)

    print(f"\nTotal robots found: {len(robots)}")

    # Show table structure
    tables = soup.find_all('table', class_='wikitable')
    print(f"\nNumber of tables found: {len(tables)}")

    # Show first few entries with full details
    print("\nFirst 10 entries (full details):")
    for i, robot in enumerate(robots[:10], 1):
        print(f"\n{i}. {robot['name']}")
        print(f"   Description: {robot['description'][:100]}...")

    # Count unique first letters
    first_letters = Counter([r['name'][0].upper() for r in robots if r['name']])
    print("\nDistribution by first letter:")
    for letter, count in sorted(first_letters.items()):
        print(f"  {letter}: {count}")

    print("\n" + "="*80)


def print_robot_names(robots, limit=50):
    """Print robot and android names with their descriptions."""
    print("\n" + "="*80)
    print("FICTIONAL ROBOTS AND ANDROIDS FROM WIKIPEDIA")
    print("="*80)
    print(f"\nTotal robots found: {len(robots)}")
    print("\n" + "-"*80)

    # Limit the output if specified
    display_robots = robots[:limit] if limit else robots

    for i, robot in enumerate(display_robots, 1):
        name = robot['name']
        desc = robot['description']

        # Truncate long descriptions
        if len(desc) > 150:
            desc = desc[:150] + "..."

        print(f"\n{i}. {name}")
        print(f"   {desc}")

    if limit and len(robots) > limit:
        print(f"\n... and {len(robots) - limit} more robots")

    print("\n" + "="*80)


def main():
    """Main function to fetch and display robot names from Wikipedia."""
    # Fetch robot data from Wikipedia
    robots = fetch_wikipedia_robots()

    if not robots:
        print("No robots found!")
        return

    # Simple output: Print robot names with descriptions
    print_robot_names(robots, limit=50)

    # Uncomment to see detailed debug information
    # from bs4 import BeautifulSoup
    # import requests
    # url = "https://en.wikipedia.org/wiki/List_of_fictional_robots_and_androids"
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # debug_robot_info(robots, soup)


if __name__ == "__main__":
    main()
