import psycopg2
import os
from dotenv import load_dotenv

class DatabaseManager:
    def __init__(self):
        load_dotenv()  

        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            self.cursor = self.conn.cursor()
            print("Connected to the database.")
        except Exception as e:
            print("Database connection failed:", e)

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
