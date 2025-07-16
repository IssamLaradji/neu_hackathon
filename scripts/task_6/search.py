#!/usr/bin/env python3
"""
DuckDuckGo Search Script
Gets the top three search results from DuckDuckGo
"""

import sys
import time
import random
from duckduckgo_search import DDGS


def search_duckduckgo(query, max_results=3, max_retries=5, base_delay=10):
    """
    Search DuckDuckGo and return the top results with aggressive rate limiting and retry logic

    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return (default: 3)
        max_retries (int): Maximum number of retry attempts (default: 5)
        base_delay (int): Base delay between requests in seconds (default: 10)

    Returns:
        list: List of search result dictionaries
    """
    for attempt in range(max_retries):
        try:
            # Add longer random delay to avoid rate limiting
            delay = base_delay + random.uniform(5, 15)
            print(
                f"Attempt {attempt + 1}/{max_retries}: Waiting {delay:.1f} seconds before request..."
            )
            time.sleep(delay)

            with DDGS() as ddgs:
                # Try different search methods
                if attempt % 2 == 0:
                    # Try text search
                    print("Trying text search...")
                    results = list(ddgs.text(query, max_results=max_results))
                else:
                    # Try news search as alternative
                    print("Trying news search...")
                    results = list(ddgs.news(query, max_results=max_results))

                if results:
                    return results
                else:
                    print("No results found, trying alternative method...")

        except Exception as e:
            error_msg = str(e)
            print(
                f"Attempt {attempt + 1}/{max_retries}: Error searching DuckDuckGo: {error_msg}"
            )

            # If it's a rate limit error, wait much longer before retrying
            if "202" in error_msg or "ratelimit" in error_msg.lower():
                wait_time = (
                    base_delay * (attempt + 1) * 3
                )  # More aggressive exponential backoff
                print(
                    f"Rate limit detected. Waiting {wait_time} seconds before retry..."
                )
                time.sleep(wait_time)
            else:
                # For other errors, wait the normal delay
                if attempt < max_retries - 1:  # Don't wait on the last attempt
                    wait_time = base_delay + random.uniform(5, 10)
                    print(
                        f"Other error detected. Waiting {wait_time:.1f} seconds before retry..."
                    )
                    time.sleep(wait_time)

    print("All retry attempts failed. Please try again later.")
    return []


def search_with_fallback(query, max_results=3):
    """
    Alternative search function with multiple fallback strategies
    """
    print("Trying alternative search strategies...")

    # Strategy 1: Try with very long delays
    print("\nStrategy 1: Extended delays...")
    results = search_duckduckgo(
        query, max_results=max_results, max_retries=3, base_delay=30
    )
    if results:
        return results

    # Strategy 2: Try with different user agent simulation
    print("\nStrategy 2: Different search approach...")
    try:
        with DDGS() as ddgs:
            # Try instant answers as fallback
            print("Trying instant answers...")
            results = list(ddgs.answers(query, max_results=max_results))
            if results:
                return results
    except Exception as e:
        print(f"Instant answers failed: {e}")

    return []


if __name__ == "__main__":
    """Main function to run the search"""
    # Get search query from command line arguments
    query = "Starcraft 2"

    print(f"Searching DuckDuckGo for: '{query}'")
    print("Note: DuckDuckGo has aggressive rate limiting. This may take a while...")

    # Perform the search with aggressive rate limiting
    results = search_duckduckgo(query, max_results=3, max_retries=5, base_delay=15)

    # If primary search fails, try fallback strategies
    if not results:
        print("\nPrimary search failed, trying fallback strategies...")
        results = search_with_fallback(query, max_results=3)

    # Display results
    if results:
        print(f"\nFound {len(results)} results:\n")

        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No URL')}")
            print(f"   Description: {result.get('body', 'No description')}")
            print("-" * 80)
    else:
        print("\nNo results found or search failed.")
        print("DuckDuckGo may be temporarily blocking requests from your IP.")
        print("Consider:")
        print("1. Waiting a few hours before trying again")
        print("2. Using a VPN or different network")
        print("3. Using an alternative search API")
