from src.models.models import Customer

def test_get_existing_customer(test_db, client):
    #test serveur +requete HTTP reussi
    response = client.get("/customers/CUS001")

    assert response.status_code == 200
    assert response.json()["customer_id"]=="CUS001"
    #test que le client existe bien dans la base de donnees
    customer = test_db.get(Customer, "CUS001")

    assert customer is not None
    assert customer.first_name == "Test"


def test_get_missing_customer(test_db, client):
    response = client.get("/customers/CUS9999")

    assert response.status_code==404
    assert response.json()["code"]=="CUSTOMER_NOT_FOUND"

    customer = test_db.get(Customer, "CUS9999")
    assert customer  is None