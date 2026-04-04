from pydantic import BaseModel, Field

class HashRequest(BaseModel):
    text: str = Field(
        title="Texto",
        description="Texto para o qual gerar o hash",
        min_length=6,
        max_length=255,
    )