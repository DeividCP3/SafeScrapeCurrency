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