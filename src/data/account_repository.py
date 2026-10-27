import sqlite3

class AccountRepository:

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_for_customer(self, customer_id):
        # Retrieve accounts belonging to a customer
        connection = self.db_manager.connect()

        try:
            connection.row_factory = sqlite3.Row
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM accounts WHERE customer_id = ?", (customer_id,))

            results = cursor.fetchall()

            return [dict(row) for row in results]
        
        finally:
            self.db_manager.close()