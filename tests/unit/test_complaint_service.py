import pytest

from src.models.models import ComplaintStatus, ComplaintCategory, Complaint, ComplaintPriority

def test_create_complaint_with_existing_customer(complaint_service, sample_complaint, fake_complaint_repository):
    result = complaint_service.create_complaint(None, sample_complaint)

    assert result.complaint_id =="CMP001"
    assert result.customer_id =="CUS001"
    assert fake_complaint_repository.get_by_id(None, "CMP001") is not None

def test_create_complaint_with_missing_customer(complaint_service, sample_complaint, fake_complaint_repository):
    setattr(sample_complaint,"customer_id", "CUS9999")
    with pytest.raises(ValueError, match="does not exist"):
        complaint_service.create_complaint(None, sample_complaint)

    assert fake_complaint_repository.get_by_id(None, "CMP001") is None

def test_create_complaint_with_missing_account(complaint_service,sample_complaint,fake_complaint_repository):
    setattr(sample_complaint, "account_id", "ACC9999")
    with pytest.raises(ValueError, match="does not exist"):
        complaint_service.create_complaint(None, sample_complaint)

    assert fake_complaint_repository.get_by_id(None, "CMP001") is None

def test_create_complaint_with_account_from_another_customer(sample_complaint, complaint_service, 
                                                             fake_complaint_repository, fake_account_repository):

    fake_account_repository.accounts["ACC001"].customer_id = "CUS002"
    setattr(sample_complaint, "account_id", "ACC001")
    with pytest.raises(ValueError, match="does not belong"):
            complaint_service.create_complaint(None, sample_complaint)
    
    assert fake_complaint_repository.get_by_id(None, "CMP001") is None


def test_create_complaint_with_valid_account(sample_complaint, complaint_service, 
                                            fake_complaint_repository):

    setattr(sample_complaint, "account_id", "ACC001")
    result = complaint_service.create_complaint(None, sample_complaint)
    
    assert fake_complaint_repository.get_by_id(None, "CMP001") is not None
    assert result.customer_id == "CUS001"
    assert result.account_id =="ACC001"


def test_get_existing_complaint(sample_complaint, complaint_service, fake_complaint_repository):
    fake_complaint_repository.create(None, sample_complaint)
    result = complaint_service.get_complaint_by_id(None, sample_complaint.complaint_id)

    assert result.customer_id == "CUS001"
    assert result.complaint_id =="CMP001"

def test_get_missing_complaint(complaint_service):
    with pytest.raises(ValueError, match="does not exist"):
        complaint_service.get_complaint_by_id(None, "CMP9999")

def test_get_all_complaint_by_existing_client(complaint_service, sample_complaint, fake_complaint_repository):
    fake_complaint_repository.create(None, sample_complaint)

    # Second complaint belongs to CUS002
    other_complaint = Complaint(
        complaint_id="CMP002",
        customer_id="CUS002",
        channel="Online",
        category=ComplaintCategory.FEE_DISPUTE,
        complaint_text="Another complaint",
        status=ComplaintStatus.OPEN,
        priority=ComplaintPriority.MEDIUM,
    )
    fake_complaint_repository.create(None, other_complaint)

    result = complaint_service.get_customer_complaints(None, "CUS001")

    assert len(result)==1
    assert result[0].customer_id=="CUS001"
    assert result[0].complaint_id =="CMP001"

def test_get_complaints_missing_customer(complaint_service):
    with pytest.raises(ValueError, match="does not exist"):
        complaint_service.get_customer_complaints(None, "CUS9999")


def test_change_status_of_existing_complaint(complaint_service, fake_complaint_repository, sample_complaint):
    fake_complaint_repository.create(None, sample_complaint)
    result = complaint_service.change_status(None, "CMP001", ComplaintStatus.IN_PROGRESS)

    assert result.status == ComplaintStatus.IN_PROGRESS
    assert fake_complaint_repository.get_by_id(None, "CMP001").status == ComplaintStatus.IN_PROGRESS


def test_invalid_change_status_of_existing_complaint(complaint_service, fake_complaint_repository, sample_complaint):
    fake_complaint_repository.create(None, sample_complaint)
    with pytest.raises(ValueError, match="Invalid transition"):
        complaint_service.change_status(None, "CMP001", ComplaintStatus.CLOSED)

    assert fake_complaint_repository.get_by_id(None, "CMP001").status == ComplaintStatus.OPEN


def test_change_status_of_missing_complaint(complaint_service):
    with pytest.raises(ValueError, match="does not exist"):
        complaint_service.change_status(None, "CMP999", ComplaintStatus.IN_PROGRESS)


def test_get_all_complaints(complaint_service,sample_complaint,fake_complaint_repository):
    fake_complaint_repository.create(None, sample_complaint)

    result = complaint_service.get_complaints(None)

    assert len(result) == 1
    assert result[0].complaint_id == "CMP001"
