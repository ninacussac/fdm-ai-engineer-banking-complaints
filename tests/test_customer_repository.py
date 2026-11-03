from src.repositories import DatabaseManager
from src.repositories.customer_repository import CustomerRepository

def main():
    db = DatabaseManager()
    customer_repo = CustomerRepository(db)

    # test non existing customer 
    customer = customer_repo.get_by_id("C1100")
    assert customer is None

    if customer is not None:
        print("Customer found:")
        print(customer)
    else:
        print("Customer not found.")

    # test existing customer
    customer = customer_repo.get_by_id("C0080")

    assert customer is not None
    assert customer["customer_id"] == "C0080"
    if customer is not None:
        print("Customer found:")
        print(customer)
    else:
        print("Customer not found.")


if __name__ == "__main__":
    main()