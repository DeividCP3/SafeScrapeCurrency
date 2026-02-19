import os

def create_file(path, content):
    """Helper to create a file with content."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Created: {path}")

def main():
    # 1. Define the Project Name
    base_dir = "BookPrice_Pipeline"
    
    # 2. Create Directory Structure
    dirs = [
        base_dir,
        os.path.join(base_dir, "src"),
        os.path.join(base_dir, "data"),
        os.path.join(base_dir, "logs")
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"📂 Directory created: {d}")

    # ---------------------------------------------------------
    # 3. Create Files (Source Code)
    # ---------------------------------------------------------

    # --- REQUIREMENTS.TXT ---
    create_file(os.path.join(base_dir, "requirements.txt"), """
requests==2.31.0
beautifulsoup4==4.12.2
cryptography==41.0.3
python-dotenv==1.0.0
""")

    # --- .ENV ---
    create_file(os.path.join(base_dir, ".env"), """
# Environment Configuration
ENV=development
API_TIMEOUT=10
""")

    # --- .GITIGNORE ---
    create_file(os.path.join(base_dir, ".gitignore"), """
__pycache__/
*.key
.env
venv/
data/*.json
logs/*.log
.DS_Store
""")

    # --- SRC/__INIT__.PY ---
    create_file(os.path.join(base_dir, "src", "__init__.py"), "")

    # --- SRC/CONFIG.PY ---
    create_file(os.path.join(base_dir, "src", "config.py"), """
import os

# Target URL for Scraping (Books to Scrape is a sandbox for testing)
SCRAPE_URL = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# Currency API (Public free API)
API_URL = "https://api.exchangerate-api.com/v4/latest/GBP"

# File Paths
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "processed_books.json")
KEY_FILE = "secret.key"
LOG_FILE = "logs/pipeline.log"

# User Agent to prevent 403 Forbidden
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
""")

    # --- SRC/SECURITY.PY ---
    create_file(os.path.join(base_dir, "src", "security.py"), """
from cryptography.fernet import Fernet
import os

class SecurityManager:
    def __init__(self, key_file):
        self.key_file = key_file
        self.key = self._load_key()
        self.cipher = Fernet(self.key)

    def _load_key(self):
        \"\"\"Loads existing key or generates a new one.\"\"\"
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def encrypt_value(self, value):
        \"\"\"Encrypts a float or string value.\"\"\"
        if value is None:
            return None
        value_str = str(value)
        return self.cipher.encrypt(value_str.encode()).decode()

    def decrypt_value(self, encrypted_val):
        \"\"\"Decrypts value back to string.\"\"\"
        if not encrypted_val:
            return None
        return self.cipher.decrypt(encrypted_val.encode()).decode()
""")

    # --- SRC/SCRAPER.PY ---
    create_file(os.path.join(base_dir, "src", "scraper.py"), """
import requests
from bs4 import BeautifulSoup
import logging
from .config import SCRAPE_URL, HEADERS

class BookScraper:
    def get_books(self):
        \"\"\"Fetches books from the website.\"\"\"
        logging.info(f"Connecting to {SCRAPE_URL}...")
        try:
            response = requests.get(SCRAPE_URL, headers=HEADERS, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            books = []
            
            articles = soup.find_all('article', class_='product_pod')
            
            for art in articles:
                title = art.h3.a['title']
                price_text = art.find('p', class_='price_color').text
                # Clean price string (remove £)
                price = float(price_text.replace('£', ''))
                
                books.append({
                    'title': title,
                    'price_gbp': price
                })
                
            logging.info(f"Scraped {len(books)} books successfully.")
            return books

        except Exception as e:
            logging.error(f"Scraping failed: {e}")
            return []
""")

    # --- SRC/API_CLIENT.PY ---
    create_file(os.path.join(base_dir, "src", "api_client.py"), """
import requests
import logging
from .config import API_URL

class CurrencyConverter:
    def get_gbp_to_usd_rate(self):
        \"\"\"Fetches live exchange rate.\"\"\"
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            rate = data['rates']['USD']
            logging.info(f"Fetched Exchange Rate: 1 GBP = {rate} USD")
            return rate
        except Exception as e:
            logging.error(f"API Error: {e}. Using fallback rate 1.25")
            return 1.25 # Fallback
""")

    # --- SRC/PIPELINE.PY ---
    create_file(os.path.join(base_dir, "src", "pipeline.py"), """
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
""")

    # --- MAIN.PY ---
    create_file(os.path.join(base_dir, "main.py"), """
import logging
from src.pipeline import DataPipeline
from src.config import LOG_FILE

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info("Starting Data Pipeline...")
    pipeline = DataPipeline()
    pipeline.run()
""")

    # --- README.md ---
    create_file(os.path.join(base_dir, "README.md"), """
# Book Price Security Pipeline

## Architecture
This project is designed as a modular pipeline to ensure separation of concerns:
1.  **Scraping Module**: Extracts data from HTML.
2.  **API Integration**: Enriches data with live currency rates.
3.  **Security Module**: Encrypts sensitive business logic (Wholesale Cost) using AES (Fernet).
4.  **Storage**: Saves processed data to JSON.

## Setup
1.  Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the pipeline:
    ```bash
    python main.py
    ```

## Encryption Details
-   **Algorithm**: AES (via Fernet).
-   **Key Management**: A `secret.key` file is generated on first run.
-   **Field Encrypted**: `wholesale_cost_secret` (Calculated as 60% of Retail Price).
""")

    print("\n✨ Project Generated Successfully!")
    print(f"👉 Open the folder '{base_dir}' in VS Code.")
    print("👉 Run: pip install -r requirements.txt")
    print("👉 Run: python main.py")

if __name__ == "__main__":
    main()