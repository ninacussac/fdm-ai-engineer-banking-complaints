import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from fastapi.testclient import TestClient

from src.data.connection import get_db
from src.data.base import Base
from src.models.models import Customer, Account
from src.main import app


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path/"test.db"

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread":False})

    Base.metadata.create_all(bind = engine)

    TestSession = sessionmaker(autoflush=False, autocommit = False, bind=engine)

    with TestSession() as db:
        customer = Customer(
            customer_id="CUS001",
            first_name = "Test",
            last_name = "Customer",
            email="test.customer@example.com"
        )

        account = Account(
            account_id="ACC001",
            customer_id="CUS001",
            account_number = "TEST123456",
            account_type="Checking",
            status="Active",
            opened_date = date(2026,1,1)
        )

        db.add(customer)
        db.add(account)
        db.commit()
        yield db

    engine.dispose()


@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db]=override_get_db
    app.state.testing = True
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.state.testing = False
        app.dependency_overrides.clear()