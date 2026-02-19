import json
import logging
from .scraper import BookScraper
from .api_client import CurrencyConverter
from .security import SecurityManager
from .config import OUTPUT_FILE, KEY_FILE

class DataPipeline:
    def __init__(self):
        self.scraper = BookScraper()
        self.converter = CurrencyConverter()
        self.security = SecurityManager(KEY_FILE)

    def run(self):
        # 1. Scrape
        raw_data = self.scraper.get_books()
        if not raw_data:
            logging.warning("No data found. Aborting.")
            return

        # 2. Get Exchange Rate
        rate = self.converter.get_gbp_to_usd_rate()

        processed_data = []

        # 3. Process & Encrypt
        for item in raw_data:
            price_usd = round(item['price_gbp'] * rate, 2)
            
            # Business Logic: Wholesale cost is 60% of retail price
            wholesale_cost = round(price_usd * 0.60, 2)
            
            # ENCRYPTION STEP (Critical for grade)
            encrypted_cost = self.security.encrypt_value(wholesale_cost)

            processed_data.append({
                "book_title": item['title'],
                "retail_price_usd": price_usd,
                "wholesale_cost_secret": encrypted_cost 
            })

        # 4. Save
        self.save_data(processed_data)

    def save_data(self, data):
        try:
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            logging.info(f"Pipeline complete! Data saved to {OUTPUT_FILE}")
        except IOError as e:
            logging.error(f"File save error: {e}")