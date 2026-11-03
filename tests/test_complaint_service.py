from types import SimpleNamespace
import pytest

from src.services.complaint_service import ComplaintService
from src.models.models import Complaint, ComplaintStatus

class FakeCustomerRepository:

    def get_by_id(self, db, customer_id):

        if customer_id in ("CUS001", "CUS002"):
            return SimpleNamespace(
                customer_id=customer_id
            )

        return None


class FakeAccountRepository:

    def get_by_id(self, db, account_id):

        if account_id == "ACC001":
            return SimpleNamespace(
                account_id="ACC001",
                customer_id="CUS001"
            )

        return None

class FakeComplaintRepository:
    def __init__(self):
        self.complaints = []
        self.events=[]

    def create(self,db,complaint):
        self.complaints.append(complaint)
        return complaint

    def get_by_id(self, db, complaint_id):
        for complaint in self.complaints:
            if complaint.complaint_id == complaint_id:
                return complaint
        return None

    def save_status_change(self,db,complaint,event):
        self.events.append(event)
        return complaint, event




def test_fake_customer_repository():

    repository = FakeCustomerRepository()

    existing_customer = repository.get_by_id(None, "CUS001")
    missing_customer = repository.get_by_id(None, "CUS999")

    assert existing_customer.customer_id == "CUS001"
    assert missing_customer is None


def test_fake_account_repository():

    repository = FakeAccountRepository()

    existing_account = repository.get_by_id(None, "ACC001")
    missing_account = repository.get_by_id(None, "ACC999")

    assert existing_account.account_id == "ACC001"
    assert existing_account.customer_id == "CUS001"
    assert missing_account is None



def test_fake_complaint_repository():

    repository = FakeComplaintRepository()

    complaint = SimpleNamespace(
        customer_id="CUS001",
        account_id = "ACC001",
        complaint_text = "Unexpected banking fee"
    )

    result = repository.create(None, complaint)

    assert result is complaint
    assert len(repository.complaints)==1
    assert repository.complaints[0] is complaint



def test_create_complaint_with_fake_repositories():

    complaint_repository = FakeComplaintRepository()
    account_repository = FakeAccountRepository()
    customer_repository = FakeCustomerRepository()

    service = ComplaintService(
        complaint_repository=complaint_repository,
        account_repository=account_repository,
        customer_repository=customer_repository,
    )


    complaint_data = SimpleNamespace(
        customer_id="CUS001",
        account_id="ACC001",
        channel="Phone",
        category="Fee Dispute",
        complaint_text="Unexpected banking fee",
        status="OPEN",
        priority="High"
    )

    # Create the complaint
    result = service.create_complaint(None, complaint_data)

    assert result is complaint_data
    assert len(complaint_repository.complaints)==1
    assert complaint_repository.complaints[0] is complaint_data



def test_create_complaint_unknown_customer():

    complaint_repository = FakeComplaintRepository()
    service = ComplaintService(
        complaint_repository=complaint_repository,
        account_repository=FakeAccountRepository(),
        customer_repository=FakeCustomerRepository(),
    )

    complaint_data = SimpleNamespace(
        customer_id="CUS999",
        account_id="ACC001",
    )

    with pytest.raises(ValueError, match="Customer CUS999 does not exist"):
        service.create_complaint(None, complaint_data)

    assert len(complaint_repository.complaints) ==0




def test_create_complaint_unknown_account():

    complaint_repository = FakeComplaintRepository()

    service = ComplaintService(
        complaint_repository=complaint_repository,
        account_repository=FakeAccountRepository(),
        customer_repository=FakeCustomerRepository()
    )

    complaint_data = SimpleNamespace(
        customer_id="CUS001",
        account_id = "ACC999"
    )

    with pytest.raises(ValueError, match = "Account ACC999 does not exist"):
        service.create_complaint(None, complaint_data)

    assert len(complaint_repository.complaints) == 0


def test_create_complaint_wrong_account_owner():

    complaint_repository = FakeComplaintRepository()

    service = ComplaintService(
        complaint_repository=complaint_repository,
        account_repository=FakeAccountRepository(),
        customer_repository=FakeCustomerRepository()
    )

    complaint_data = SimpleNamespace(
        customer_id="CUS002",
        account_id = "ACC001"
    )

    with pytest.raises(ValueError, match = "Account ACC001 does not belong to customer CUS002"):
        service.create_complaint(None, complaint_data)

    assert len(complaint_repository.complaints) == 0



def test_get_unknown_complaint():

    service = ComplaintService(
        complaint_repository=FakeComplaintRepository(),
        customer_repository=FakeCustomerRepository(),
        account_repository=FakeAccountRepository()
    )

    with pytest.raises(
        ValueError,
        match="Complaint CMP999 does not exist"
    ):
        service.get_complaint_by_id(None, "CMP999")


def test_service_valid_status_transition():

    complaint_repository = FakeComplaintRepository()

    complaint = Complaint(
        complaint_id="CMP001",
        status=ComplaintStatus.OPEN
    )

    complaint_repository.complaints.append(complaint)

    service = ComplaintService(
        complaint_repository=complaint_repository,
        customer_repository=FakeCustomerRepository(),
        account_repository=FakeAccountRepository()
    )

    updated_complaint, event = service.change_status(
        db=None,
        complaint_id="CMP001",
        new_status=ComplaintStatus.IN_PROGRESS,
        changed_by="analyst001",
        comments="Investigation started"
    )

    assert updated_complaint.status == ComplaintStatus.IN_PROGRESS
    assert event.complaint_id == "CMP001"
    assert event.old_status == ComplaintStatus.OPEN
    assert event.new_status == ComplaintStatus.IN_PROGRESS
    assert event.changed_by == "analyst001"
    assert event.comments == "Investigation started"
    assert len(complaint_repository.events) == 1
    assert complaint_repository.events[0] is event


def test_service_invalid_status_transition():

    complaint_repository = FakeComplaintRepository()

    complaint = Complaint(
        complaint_id="CMP001",
        status=ComplaintStatus.OPEN
    )

    complaint_repository.complaints.append(complaint)

    service = ComplaintService(
        complaint_repository=complaint_repository,
        customer_repository=FakeCustomerRepository(),
        account_repository=FakeAccountRepository()
    )
    new_status = ComplaintStatus.CLOSED
    with pytest.raises(ValueError,match=f"Invalid transition: {complaint.status.value} -> {new_status.value}"):
        service.change_status(
            db=None,
            complaint_id="CMP001",
            new_status=new_status,
        )

    assert complaint.status == ComplaintStatus.OPEN
    assert len(complaint_repository.events) == 0


def test_service_change_status_unknown_complaint():

    complaint_repository = FakeComplaintRepository()
    service = ComplaintService(
        complaint_repository=complaint_repository,
        customer_repository=FakeCustomerRepository(),
        account_repository=FakeAccountRepository()
    )

    with pytest.raises(ValueError, match="Complaint CMP999 does not exist"):
        service.change_status(None, complaint_id="CMP999", new_status=ComplaintStatus.IN_PROGRESS)

    assert len(complaint_repository.events)==0