import requests
from bs4 import BeautifulSoup
import os
import time


def get_wikipedia_content(url):
    """
    Retrieve content from a Wikipedia page using BeautifulSoup
    """
    try:
        # Add headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the main content div (usually with id 'mw-content-text')
        content_div = soup.find("div", {"id": "mw-content-text"})

        if not content_div:
            return "Could not find main content on the page."

        # Extract text from paragraphs, removing references and other non-content elements
        paragraphs = []
        for element in content_div.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
            # Skip elements that are typically not main content
            if (
                element.find_parent("div", {"class": "reflist"})
                or element.find_parent("div", {"class": "refbegin"})
                or element.find_parent("div", {"class": "refend"})
                or element.find_parent("table", {"class": "wikitable"})
            ):
                continue

            text = element.get_text(strip=True)
            if text and len(text) > 50:  # Only include substantial paragraphs
                paragraphs.append(text)

        return "\n\n".join(paragraphs)

    except requests.RequestException as e:
        return f"Error retrieving content: {e}"
    except Exception as e:
        return f"Error parsing content: {e}"


def save_content_to_file(content, filename):
    """
    Save content to a text file
    """
    try:
        # Create results directory if it doesn't exist
        os.makedirs("results", exist_ok=True)

        filepath = os.path.join("results", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Content saved to {filepath}")

    except Exception as e:
        print(f"Error saving to {filename}: {e}")


def main():
    """
    Main function to retrieve content from 3 Wikipedia pages about knights
    """
    # Wikipedia pages related to knights
    knight_pages = [
        "https://en.wikipedia.org/wiki/Knight",
        "https://en.wikipedia.org/wiki/Knights_Templar",
        "https://en.wikipedia.org/wiki/Medieval_warfare",
    ]

    print("Retrieving content from Wikipedia pages about knights...")

    for i, url in enumerate(knight_pages, 1):
        print(f"\nProcessing page {i}: {url}")

        # Get the content
        content = get_wikipedia_content(url)

        # Save to file
        filename = f"page_{i}.txt"
        save_content_to_file(content, filename)

        # Add a small delay to be respectful to Wikipedia's servers
        if i < len(knight_pages):
            time.sleep(2)

    print("\nAll pages have been processed and saved to the results directory!")


if __name__ == "__main__":
    main()
