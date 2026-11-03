from src.repositories import DatabaseManager

def main():
    db = DatabaseManager()

    ## Test for commit 
    try:

        connection = db.connect()
        print("Database connected successfully!")

        c = connection.cursor() # cursor
        c.execute("INSERT INTO complaint (customer_id, category) VALUES (?, ?)", (1, "Test complaint"))

        inserted_id = c.lastrowid

        db.commit()
        print("Changes committed successfully!")

    except Exception as e:

        print(f"An error occurred: {e}")
        db.rollback()
        print("Changes rolled back due to an error.")

    finally:

        db.close()
        print("Database connection closed.")

    ## Test for rollback    
    try:
        connection = db.connect()
        print("Database connected successfully!")

        c = connection.cursor()

        # Insert a test complaint
        c.execute(
            "INSERT INTO complaint (customer_id, category) VALUES (?, ?)",
            (1, "Rollback test complaint")
        )

        inserted_id = c.lastrowid
        print(f"Inserted complaint ID: {inserted_id}")

        # Cancel the insertion
        db.rollback()
        print("Changes rolled back successfully!")

        # Verify that the complaint no longer exists
        c.execute(
            "SELECT * FROM complaint WHERE rowid = ?",
            (inserted_id,)
        )

        result = c.fetchone()

        if result is None:
            print("PASS: The complaint was not saved.")
        else:
            print("FAIL: The complaint still exists.")

    except Exception as e:
        print(f"An error occurred: {e}")

        if db.connection is not None:
            db.rollback()

    finally:
        db.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()