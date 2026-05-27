from pydantic import BaseModel

class SwordsSchema(BaseModel):
    id: int | None = None
    title: str
    description: str