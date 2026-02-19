import requests
from bs4 import BeautifulSoup
import logging
from .config import SCRAPE_URL, HEADERS

class BookScraper:
    def get_books(self):
        """Fetches books from the website."""
        logging.info(f"Connecting to {SCRAPE_URL}...")
        try:
            response = requests.get(SCRAPE_URL, headers=HEADERS, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            books = []
            
            articles = soup.find_all('article', class_='product_pod')
            
            for art in articles:
                title = art.h3.a['title']
                price_tag = art.find('p', class_='price_color')
                
                if price_tag:
                    # FIX: Handle both the Pound symbol and the 'Â' encoding artifact
                    raw_price = price_tag.get_text()
                    clean_price = raw_price.replace('£', '').replace('Â', '').strip()
                    
                    try:
                        price = float(clean_price)
                    except ValueError:
                        # Safety Net: If cleaning fails, strip everything except numbers and dots
                        import re
                        price = float(re.sub(r'[^\d.]', '', clean_price))
                    
                    books.append({
                        'title': title,
                        'price_gbp': price
                    })
                
            logging.info(f"Scraped {len(books)} books successfully.")
            return books

        except Exception as e:
            logging.error(f"Scraping failed: {e}")
            return []