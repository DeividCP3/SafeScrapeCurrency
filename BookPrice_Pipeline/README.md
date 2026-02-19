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