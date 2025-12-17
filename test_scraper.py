import sys
import os

# Adjust path to find backend module
sys.path.append(os.getcwd())

from backend.agent.hashtag_scraper import scrape_hashtags

def test_scraper():
    # Test complex query that previously failed
    query = "food, sandwiches, snacks, chips" 
    print(f"Testing scraper for complex query: '{query}'")
    tags = scrape_hashtags(query)
    print(f"Tags found: {len(tags)}")
    print(tags)
    
    if len(tags) > 0:
        print("✅ Complex query test PASSED (Sanitization worked)")
    else:
        print("❌ Complex query test FAILED")

    # Test single word
    query2 = "marketing"
    print(f"\nTesting scraper for simple query: '{query2}'")
    tags2 = scrape_hashtags(query2)
    print(f"Tags found: {len(tags2)}")
    
    if len(tags2) > 0:
        print("✅ Simple query test PASSED")

if __name__ == "__main__":
    test_scraper()
