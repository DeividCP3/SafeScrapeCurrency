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