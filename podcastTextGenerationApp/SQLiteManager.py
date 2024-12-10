import sqlite3
from datetime import datetime
from typing import Union


class SQLiteManager:
    def __init__(self, db_path="podcast_plugin.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS last_fetched (
            cleanLink TEXT PRIMARY KEY,
            lastFetched TEXT
        )
        """
        with self.connection:
            self.connection.execute(query)

    def get_last_fetched(self, cleanLink) -> Union[datetime, None]:
        query = "SELECT lastFetched FROM last_fetched WHERE cleanLink = ?"
        cursor = self.connection.execute(query, (cleanLink))
        result = cursor.fetchone()
        if result:
            return datetime.fromisoformat(result[0])
        return None

    def set_last_fetched(self, cleanLink, lastFetched):
        query = """
        INSERT INTO last_fetched (cleanLink, lastFetched) 
        VALUES (?, ?) 
        ON CONFLICT(cleanLink) 
        DO UPDATE SET lastFetched = excluded.lastFetched
        """
        with self.connection:
            self.connection.execute(query, (cleanLink, lastFetched))

    def close(self):
        self.connection.close()
