
from src.models.models import CaseNote, AuditEvent


class CaseNoteRepository:

    def create(self, db, complaint_id, note, evidence_refs, actor_id):
        try:
            case_note = CaseNote(
                complaint_id=complaint_id,
                note=note,
                evidence_refs=evidence_refs,
                created_by=actor_id)
            db.add(case_note)
            db.flush()

            #Create the audit event
            audit_event = AuditEvent(
                complaint_id=complaint_id,
                action="CREATE_CASE_NOTE",
                actor_id=actor_id,
                details={"note_id": case_note.note_id})
            db.add(audit_event)
            db.flush()

            result = {
                "note_id": case_note.note_id,
                "complaint_id": case_note.complaint_id,
                "audit_id": audit_event.audit_id,
            }
            db.commit()
            return result

        except Exception:
            db.rollback()
            raise