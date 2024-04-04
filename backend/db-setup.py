from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file
username = os.getenv('PG_USERNAME')
password = os.getenv('PG_PASSWORD')
password = os.getenv('PG_HOSTNAME')
password = os.getenv('PG_PORT')
password = os.getenv('PG_DB')
password = os.getenv('PG_EXTERNAL_DB_URL')
