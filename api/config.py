import os
from google.oauth2 import service_account

# Google Cloud Platform service account settings:
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
CREDENTIALS = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

# BigQuery variables:
BQ_DATASET = 'stock_data'
BQ_TABLE = 'prices'
