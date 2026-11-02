import pytest

from src.models.models import ComplaintStatus

# permet d'exec le meme test avec pls jeux de donnees
@pytest.mark.parametrize("initial_status, new_status",
                         [
                             (ComplaintStatus.OPEN, ComplaintStatus.IN_PROGRESS),
                             (ComplaintStatus.IN_PROGRESS, ComplaintStatus.UNDER_REVIEW),
                             (ComplaintStatus.UNDER_REVIEW, ComplaintStatus.CLOSED),
                         ],)
def test_valid_status_transition(sample_complaint, initial_status, new_status):
    sample_complaint.status=initial_status
    event = sample_complaint.change_status(new_status)

    assert sample_complaint.status == new_status
    assert event.old_status == initial_status
    assert event.new_status == new_status

# permet d'exec le meme test avec pls jeux de donnees
@pytest.mark.parametrize("initial_status, new_status",
                         [
                             (ComplaintStatus.OPEN, ComplaintStatus.CLOSED),
                             (ComplaintStatus.OPEN, ComplaintStatus.UNDER_REVIEW),
                             (ComplaintStatus.IN_PROGRESS, ComplaintStatus.OPEN),
                             (ComplaintStatus.CLOSED, ComplaintStatus.OPEN),
                         ],)
def test_invalid_status_transition(sample_complaint, initial_status, new_status):
    sample_complaint.status=initial_status
    # On attend une erreur
    with pytest.raises(ValueError):
        sample_complaint.change_status(new_status)

    assert sample_complaint.status == initial_status


@pytest.mark.parametrize("field, invalid_value", 
                         [
                             ("status", "INVALID"), 
                             ("category", "Unknown"), 
                             ("priority", "Urgent")
                         ])
def test_invalid_complaint_fields(sample_complaint, field, invalid_value):
    with pytest.raises(ValueError):
        setattr(sample_complaint, field, invalid_value) # modif l'attribut d'un objet en utilisant son nom

def test_complaint_accepts_no_priority(sample_complaint):
    sample_complaint.priority = None
    assert sample_complaint.priority is None
