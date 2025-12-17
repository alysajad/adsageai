import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_hashtags(query):
    """
    Scrapes hashtags for a given query from best-hashtags.com.
    Returns a list of unique hashtags.
    """
    if not query:
        return []

    try:
        # Sanitize query: take the first comma-separated part, then the first space-separated word
        # best-hashtags.com generally only supports single-word slugs
        if ',' in query:
            query = query.split(',')[0]
        
        query = query.strip().split()[0]
        
        # Encode the query (e.g. "social media" -> "social+media" - actually checking above, we know it fails often with +, so single word is safer)
        encoded_query = urllib.parse.quote_plus(query.strip())
        url = f"https://best-hashtags.com/hashtag/{encoded_query}/"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        hashtags = []
        
        # Strategy 1: Look for the specific copy-paste blocks usually found on this site
        # They often have a class like 'tag-box' or just lists inside text areas
        # Inspecting the typical structure of best-hashtags.com:
        # It usually lists hashtags in paragraph tags or specific div containers.
        # Let's try to find text content that looks like a list of hashtags.
        
        # Based on previous reading: "Top 10 marketing hashtags" -> list of links
        # The content was: #marketing - 43% + #business - 8% ...
        
        # Let's extract from the text content of the page where we see "#"
        # A more robust way given the HTML structure is usually looking for specific elements.
        # But since I don't have the full HTML, I'll use a regex-like approach on the text specific sections 
        # or look for the 'p1', 'p2' classes usually used there if I recall correctly, 
        # OR just find all words starting with # in the main content area.
        
        # Let's try to target the easy-to-copy lists often present.
        # Example structure: <div class="col-md-12"> <p class="1"> #marketing #business ... </p> </div>
        
        # Fallback generic extraction:
        content_divs = soup.find_all('div', class_='col-sm-12') # Common container
        
        for div in content_divs:
            text = div.get_text()
            words = text.split()
            for word in words:
                if word.startswith('#') and len(word) > 2 and word not in hashtags:
                     # Clean punctuation
                    clean_tag = word.strip(".,!?:;\"'()[]{}")
                    if clean_tag.startswith('#'):
                        hashtags.append(clean_tag)
                        if len(hashtags) >= 20: # Limit to top 20
                            break
            if len(hashtags) >= 20:
                break
                
        # If specific container didn't yield enough, generic search on page:
        if len(hashtags) < 5:
             all_text = soup.get_text()
             words = all_text.split()
             for word in words:
                 if word.startswith('#') and len(word) > 2 and word not in hashtags:
                     clean_tag = word.strip(".,!?:;\"'()[]{}")
                     if clean_tag.startswith('#') and clean_tag.lower() != '#hashtags':
                         hashtags.append(clean_tag)
                         if len(hashtags) >= 20:
                             break

        return hashtags

    except Exception as e:
        print(f"Error scraping hashtags for '{query}': {e}")
        return []
