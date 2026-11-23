from pydantic import BaseModel, Field

class CaseNoteCreate(BaseModel):
    note: str = Field(min_length=1,description="Content of the case note.")
    evidence_refs: list[str] = Field(default_factory=list,
        description="References to supporting evidence.")
