import logging
import requests
from bs4 import BeautifulSoup

class Tools:
    def __init__(self):
        """Initialize tools for agent use."""
        self.search_engine_url = "https://www.google.com/search?q="

    def search_google(self, query):
        """Scrape Google Search results for real-time fact-checking."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            search_url = self.search_engine_url + "+".join(query.split())
            response = requests.get(search_url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                snippets = soup.find_all("span", class_="aCOpRe")
                
                if snippets:
                    return snippets[0].text  # ✅ Return first search result snippet
                else:
                    return None
        except Exception as e:
            logging.error(f"Error fetching web data: {e}")
            return None
