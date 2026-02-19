import requests
import logging
from .config import API_URL

class CurrencyConverter:
    def get_gbp_to_usd_rate(self):
        """Fetches live exchange rate."""
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