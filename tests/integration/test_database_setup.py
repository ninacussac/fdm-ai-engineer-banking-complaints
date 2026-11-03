from src.models.models import Customer, Account

def test_database_contains_seed_data(test_db):
    customer = test_db.get(Customer, "CUS001")
    account = test_db.get(Account, "ACC001")

    assert customer is not None
    assert account is not None
    assert customer.customer_id == account.customer_id