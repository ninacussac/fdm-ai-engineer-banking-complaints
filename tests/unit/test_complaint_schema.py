import pytest
from pydantic import ValidationError

from src.schemas.complaint_schema import ComplaintCreate

@pytest.mark.parametrize(
    "missing_field",
    [
        "customer_id", 
        "channel", 
        "category",
        "complaint_text",
        "status",
        "priority"
    ]
)
def test_missing_required_field(missing_field):

    complaint_data = {
        "customer_id": "CUS001",
        "channel": "Online",
        "category": "Fee Dispute",
        "complaint_text": "Incorrect fee charged",
        "status": "OPEN",
        "priority": "Medium",
    }

    complaint_data.pop(missing_field)

    with pytest.raises(ValidationError):
        ComplaintCreate(**complaint_data) #transforme les elements du dictionnaire en argument construire l'objet pydantic

def test_optionnal_fields_can_be_omitted():
    complaint_data = {
        "customer_id": "CUS001",
        "channel": "Online",
        "category": "Fee Dispute",
        "complaint_text": "Incorrect fee charged",
        "status": "OPEN",
        "priority": "Medium",
    }

    complaint = ComplaintCreate(**complaint_data)

    assert complaint.account_id is None
    assert complaint.assigned_analyst_id is None
    assert complaint.received_at is not None