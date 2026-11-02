
import pytest

from src.models.models import Complaint,ComplaintStatus,ComplaintCategory,ComplaintPriority, Account
from src.services.complaint_service import ComplaintService

@pytest.fixture
def sample_complaint():
    return Complaint(
        complaint_id="CMP001",
        customer_id="CUS001",
        channel="Online",
        category=ComplaintCategory.FEE_DISPUTE,
        complaint_text="Incorrect fee charged",
        status=ComplaintStatus.OPEN,
        priority=ComplaintPriority.MEDIUM,
    )


class FakeCustomerRepository:
    def __init__(self):
        self.customers = {"CUS001": object()}

    def get_by_id(self, db, customer_id):
        return self.customers.get(customer_id)


@pytest.fixture
def fake_customer_repository():
    return FakeCustomerRepository()

class FakeAccountRepository:
    def __init__(self):
        self.accounts = {"ACC001": Account(account_id="ACC001",customer_id="CUS001",)}

    def get_by_id(self, db, account_id):
        return self.accounts.get(account_id)


@pytest.fixture
def fake_account_repository():
    return FakeAccountRepository()


class FakeComplaintRepository:
    def __init__(self):
        self.complaints = {}

    def create(self, db, complaint):
        self.complaints[complaint.complaint_id] = complaint
        return complaint

    def get_all(self, db):
        return list(self.complaints.values())

    def get_by_id(self, db, complaint_id):
        return self.complaints.get(complaint_id)

    def get_by_customer_id(self, db, customer_id):
        return [
            complaint
            for complaint in self.complaints.values()
            if complaint.customer_id == customer_id
        ]

    def save_status_change(self, db, complaint, event):
        self.complaints[complaint.complaint_id] = complaint
        return complaint


@pytest.fixture
def fake_complaint_repository():
    return FakeComplaintRepository()

@pytest.fixture
def complaint_service(fake_complaint_repository,fake_customer_repository,fake_account_repository):
    return ComplaintService(fake_complaint_repository,fake_customer_repository,fake_account_repository)