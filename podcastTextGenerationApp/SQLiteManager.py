
import sqlite3
import os

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

    def get_last_fetched(self, cleanLink):
        query = "SELECT lastFetched FROM last_fetched WHERE cleanLink = ?"
        cursor = self.connection.execute(query, (cleanLink,))
        result = cursor.fetchone()
        return result[0] if result else None

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
