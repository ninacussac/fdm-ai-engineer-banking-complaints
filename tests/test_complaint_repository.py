from src.data import DatabaseManager
from src.data.complaint_repository import ComplaintRepository
import sqlite3

def main():
    db = DatabaseManager()
    complaint_repo = ComplaintRepository(db)

    # # test get_by_id() complaint
    customer_id_ok = "CP00026"
    complaints = complaint_repo.get_by_id(customer_id_ok)
    assert complaints is not None
    assert complaints["complaint_id"] == customer_id_ok
    if complaints :
        print(complaints)
    else:
        print("No complaint found for this complaint_id.")

    
    # test get_by_id() complaint non existing
    complaints = complaint_repo.get_by_id("CP9999")
    assert complaints is None
    if complaints :
        print(complaints)
    else:
        print("No complaint found for this complaint_id.")

    # test get_for_customer existing customer
    customer_id_pass = "C0079"
    cus_complaints = complaint_repo.get_for_customer(customer_id_pass)

    assert len(cus_complaints) > 0
    assert all(
        complaint["customer_id"] == customer_id_pass
        for complaint in cus_complaints
    )
    if cus_complaints :
        print(f"Found {len(cus_complaints)} complaint(s):")
        for complaint in cus_complaints:
            print(complaint)
    else:
        print("No complaint found for this customer.")

    # test get_for_customer non existing customer
    cus_complaints = complaint_repo.get_for_customer("C9999")
    assert cus_complaints == []
    if cus_complaints :
        print(f"Found {len(cus_complaints)} complaint(s):")
        for complaint in cus_complaints:
            print(complaint)
    else:
        print("No complaint found for this customer.")


    # test create : successfull scenario
    
    complaint_repo.create(
    customer_id="C0079",
    category="Fraud Claim",
    channel="Email",
    status="OPEN",
    date_opened="2025-03-01 10:00:00",
    priority="Medium"
    )

    try: 
        connection = db.connect()
        connection.row_factory = sqlite3.Row
        c = connection.cursor()
        c.execute(
            "SELECT * FROM complaint WHERE customer_id = ? AND category= ?",
            ("C0079","Fraud Claim" )
        )
        
        result = c.fetchone()
        assert result is not None, "Complaint was not inserted."
        assert result["complaint_id"] is not None
        assert result["complaint_id"].startswith("C")

    finally:
        
        db.close()

    # Test create() - Failure scenario
    try:
        complaint_repo.create(
            customer_id="CUS009",
            category="Fraud Claim",
            channel="Email",
            status=None,
            date_opened=None,
            priority="Medium"
        )

        assert False, "Expected an SQLite error."

    except sqlite3.IntegrityError:
        print("PASS: Invalid insertion was rejected.")
        connection = db.connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM complaint WHERE category = ? AND date_opened IS ? ",
            ("Fraud Claim",None)
        )

        assert cursor.fetchone()[0] == 0

    finally:
        db.close()




if __name__ == "__main__":
    main()