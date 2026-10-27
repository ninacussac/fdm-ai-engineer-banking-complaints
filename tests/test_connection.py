from src.data import DatabaseManager

def main():
    db = DatabaseManager()

    try:
        connection = db.connect()
        print("Database connected successfully!")

    finally:
        db.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()