import psycopg
import os
import pathlib
import dotenv
BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
dotenv.load_dotenv(BASE_DIR / ".env")
def db_connect():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("USER_NAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("HOST"),
    )