from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError


load_dotenv_success = load_dotenv()
if load_dotenv_success:
    print("Environment variables loaded successfully.")
else:
    print("Failed to load .env file.")


pg_username = os.getenv('PG_USERNAME')
pg_password = os.getenv('PG_PASSWORD')
pg_hostname = os.getenv('PG_HOSTNAME')
pg_port = os.getenv('PG_PORT')
pg_db = os.getenv('PG_DB')
pg_external_db_url = os.getenv('PG_EXTERNAL_DB_URL')

def create_connection():
    try:
        if pg_external_db_url:
            conn = psycopg2.connect(pg_external_db_url)
        else:
            conn = psycopg2.connect(
                host=pg_hostname,
                database=pg_db,
                user=pg_username,
                password=pg_password,
                port=pg_port
            )
        print("Connection to PostgreSQL DB successful")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

connection = create_connection()

connection.close()
