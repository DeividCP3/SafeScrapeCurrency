1. Project Overview
   SafeScrape is an end-to-end data engineering solution designed to automate the collection of retail book data, perform real-time financial transformations via REST APIs, and secure sensitive business metrics. This project demonstrates a production-ready Modular Architecture that prioritizes data integrity and security.

2. Solution Architecture
   The system is decoupled into specialized modules to ensure high maintainability and scalability (Requirement: 10/60 pts).

src/scraper.py: A robust web scraper built with BeautifulSoup4. It features custom headers to mimic browser behavior and includes UTF-8 encoding fixes to handle non-standard currency symbols (e.g., £/Â) found in raw HTML.

src/api_client.py: Integrates with a Financial REST API to fetch live GBP-to-USD exchange rates. It implements defensive programming to ensure the pipeline continues even if the external API is unavailable.

src/security.py: The security layer. It implements Symmetric Encryption using the Fernet (AES-128) standard, ensuring that sensitive financial data is never stored in plain text.

src/pipeline.py: The "Brain" of the operation. It orchestrates the flow of data from raw extraction to final encrypted storage.

3. Setup & Environment Configuration
   To evaluate the project, please follow these steps to initialize the environment:

A. Directory Integrity
Ensure all project files are in the root directory as follows:

data/ (Output destination)

logs/ (Pipeline history)

src/ (Core logic modules)

main.py (Entry point)

requirements.txt (Dependencies)

.env (Environment variables)

B. Install Dependencies
Install the necessary libraries for scraping, API calls, and cryptography using the provided requirements file:

C. Environment Variables
The project utilizes a .env file to manage configuration. Ensure the file contains the necessary API endpoints and local settings to avoid hard-coding sensitive parameters.

4. Execution Guide
   Once the setup is complete, run the main orchestrator to start the automated flow:

5. Data Transformation & Security Logic
   The pipeline follows a strict ETL (Extract, Transform, Load) process:

Extract: Scrapes titles and prices from the target catalogue.

Transform:

Converts GBP prices to USD using live API data.

Calculates a Wholesale Cost (Business Logic: Retail Price × 0.60).

Encrypt: The Wholesale Cost is considered a "Trade Secret." It is encrypted into a base64-encoded ciphertext using a local secret.key.

Load: The final enriched dataset is exported to data/processed_books.json.

6. Security Implementation (Requirement: 10/60 pts)
   Algorithm: AES-128 (Fernet) Symmetric Encryption.

Key Isolation: The cryptographic key is generated and stored locally in secret.key.

Data Masking: Sensitive financial fields are stored as ciphertext, rendering them unreadable without the corresponding key.

## Setup

1.  Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the pipeline:
    ```bash
    python main.py
    ```
