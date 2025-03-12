import json
import logging
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s- %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_storeage_client():
    try:
        # Path to the GCP JSON credentials file
        credentials_path = 'C:\Users\mike-\OneDrive\projects\data_engeneering\data_weather_project\gcp_credential.json'

        with open(credentials_path, 'r') as f:
            json_credentials = json.load(f)
        
        # Create credentials from the dictionary
        credentials = service_account.Credentials.from_service_account_info(json_credentials)

        # Create and return a storage client using the explicit credentials
        storage_client = storage.Client(credentials=credentials)
        return storage_client
    
    except Exception as e:
        logger.error(f"Error creating sotrage client: {str(e)}")
        raise

def export_to_cloud_storage(data, bucket_name, blob_name):
    """Exports data to Google Cloud Storage as a CSV file"""
    try:
        # Convert data to Pandas Dataframe
        df = pd.DataFrame(data)

        # Create an in-memory CSV file
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Initialize Google Cloud Storage client
        storage_client = get_storeage_client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name + '.csv')

        # Upload the CSV data to GCS
        blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
        logger.info(f"Data sucessfully exported to gs;//{bucket_name}/{blob_name}.csv")

    except Exception as e:
        logger.error(f"Error exporting data to Cloud Storage {str(e)}")
        raise