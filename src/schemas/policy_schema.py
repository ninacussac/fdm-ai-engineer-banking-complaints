from pydantic import BaseModel, Field, field_validator

class PolicyQuery(BaseModel):
    question: str = Field(min_length=1)
    document_type: str | None = None
    effective_version: str | None = None
    access_label: str | None = None

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question cannot be empty")
        return value.strip()
