import sqlite3

class ComplaintRepository:

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_by_id(self, complaint_id):
        # Retrieve a complaint by ID
        connection = self.db_manager.connect()
        try:
            connection.row_factory = sqlite3.Row
            c = connection.cursor()
            c.execute(
                "SELECT * FROM complaint WHERE complaint_id = ?",
                (complaint_id,)
            )
            result = c.fetchone()
            return dict(result) if result is not None else None
        finally:
            self.db_manager.close()

    def get_for_customer(self, customer_id):
        # Retrieve all complaints for a customer
        connection = self.db_manager.connect()
        try:
            connection.row_factory = sqlite3.Row
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM complaint WHERE customer_id = ?", (customer_id,))

            results = cursor.fetchall()

            return [dict(row) for row in results]
        
        finally:
            self.db_manager.close()


    def create(
        self,
        customer_id,
        category,
        channel,
        status,
        received_at,
        complaint_text,
        priority,
        account_id=None,
    ):
        connection = self.db_manager.connect()

        try:
            cursor = connection.cursor()

            # Generate the next complaint ID
            cursor.execute("""
                SELECT MAX(
                    CAST(SUBSTR(complaint_id, 4) AS INTEGER)
                )
                FROM complaint
                WHERE complaint_id GLOB 'CMP[0-9]*'
            """)

            max_number = cursor.fetchone()[0]
            next_number = (max_number or 0) + 1
            new_complaint_id = f"CMP{next_number:03d}"

            # Insert new complaint
            cursor.execute("""
                INSERT INTO complaint (
                    complaint_id,
                    customer_id,
                    account_id,
                    channel,
                    category,
                    complaint_text,
                    priority,
                    status,
                    received_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_complaint_id,
                customer_id,
                account_id,
                channel,
                category,
                complaint_text,
                priority,
                status,
                received_at
            ))

            self.db_manager.commit()

            return new_complaint_id

        except sqlite3.Error:
            self.db_manager.rollback()
            raise

        finally:
            self.db_manager.close()
