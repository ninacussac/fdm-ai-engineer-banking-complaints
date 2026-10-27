import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

class DatabaseManager:

    def __init__(self):
        
        # Load and validate database configuration
        
        PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
        load_dotenv(PROJECT_ROOT / ".env")
        db_path = os.getenv("DB_TEST_PATH")
        if not db_path:
            raise ValueError("DB_TEST_PATH environment variable is not defined.")
        
        self.db_path = PROJECT_ROOT / db_path
        if not self.db_path.is_file():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        
        self.connection = None


    def connect(self):
        # Open a database connection
        if self.connection is not None:
            raise RuntimeError("Database connection is already open.")
        
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection


    def close(self):
        # Close the database connection safely
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def commit(self):
        # Save transaction changes
        if self.connection is None:
            raise RuntimeError("No active database connection.")
        self.connection.commit()

    def rollback(self):
        # Cancel transaction changes
        if self.connection is None:
            raise RuntimeError("No active database connection.")
        self.connection.rollback()