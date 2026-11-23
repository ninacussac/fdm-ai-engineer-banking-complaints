
from src.repositories.case_note_repository_sqlalchemy import CaseNoteRepository
from src.repositories.complaint_repository_sqlalchemy import ComplaintRepository


class CaseNoteService:
    ALLOWED_ROLES = {"Analyst", "Supervisor"}

    def __init__(self):
        self.case_note_repository = CaseNoteRepository()
        self.complaint_repository = ComplaintRepository()

    def create_case_note(
        self,
        db,
        complaint_id: str,
        note: str,
        evidence_refs: list[str],
        actor_id: str,
        actor_role: str,
    ) -> dict:

        if actor_role not in self.ALLOWED_ROLES:
            raise PermissionError(
                "Only Analysts and Supervisors can create case notes."
            )

        if not isinstance(actor_id, str) or not actor_id.strip():
            raise PermissionError("Missing authenticated actor.")

        if not isinstance(complaint_id, str) or not complaint_id.strip():
            raise ValueError("Invalid complaint ID.")

        if not isinstance(note, str) or not note.strip():
            raise ValueError("Case note cannot be empty.")

        if (
            not isinstance(evidence_refs, list)
            or any(
                not isinstance(ref, str) or not ref.strip()
                for ref in evidence_refs
            )
        ):
            raise ValueError("Invalid evidence references.")

        complaint = self.complaint_repository.get_by_id(db, complaint_id)

        if complaint is None:
            raise ValueError(f"Complaint {complaint_id} does not exist.")

        return self.case_note_repository.create(
            db=db,
            complaint_id=complaint_id,
            note=note.strip(),
            evidence_refs=evidence_refs,
            actor_id=actor_id,
        )
