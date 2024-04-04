from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import psycopg2.extras


def get_connection(): 
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
        print("Connection to PostgreSQL DB successful.")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return(conn)


def create_scripts_table(connection):
    if connection is not None:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scripts (
                    title VARCHAR(255),
                    line_id INTEGER,
                    line_text TEXT,
                    vector_data FLOAT[]
                );
            """)
            connection.commit()


def insert_script_data(connection, scripts, batch_size=1000):
    if connection is not None:
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE scripts;")
            for start in range(0, len(scripts), batch_size):
                end = start + batch_size
                chunk = scripts.iloc[start:end]
                data_tuples = [
                    (row['Title'], row['Line ID'], row['Line Text'], [float(x) for x in row['Vector Data']])
                    for _, row in chunk.iterrows()
                ]
                psycopg2.extras.execute_batch(cursor, """
                    INSERT INTO scripts (title, line_id, line_text, vector_data)
                    VALUES (%s, %s, %s, %s);
                    """, data_tuples)
                connection.commit()
        connection.close()