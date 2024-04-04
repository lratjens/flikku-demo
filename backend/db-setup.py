from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file
pg_username = os.getenv('PG_USERNAME')
pg_password = os.getenv('PG_PASSWORD')
pg_hostname = os.getenv('PG_HOSTNAME')
pg_port = os.getenv('PG_PORT')
pg_db = os.getenv('PG_DB')
pg_external_db_url = os.getenv('PG_EXTERNAL_DB_URL')
