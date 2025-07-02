import mariadb
import os
from dotenv import load_dotenv
load_dotenv()
def get_connection():
    try:
        connection=mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv("DB_HOST"),
            port=3306,
            database=os.getenv("DB_NAME")
        )   
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to database {e}")

print(get_connection())