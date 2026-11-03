from .database_manager import DatabaseManager
import sqlite3

class CustomerRepository:

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_by_id(self, customer_id):
        # Retrieve customer information by ID
        connection = self.db_manager.connect()

        try:
            connection.row_factory = sqlite3.Row
            c = connection.cursor()
            c.execute(
                "SELECT * FROM customer WHERE customer_id = ?",
                (customer_id,)
            )
            result = c.fetchone()
            return dict(result) if result is not None else None
        finally:
            self.db_manager.close()