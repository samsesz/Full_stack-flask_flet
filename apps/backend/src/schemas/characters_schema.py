from pydantic import BaseModel

class CharactersSchema(BaseModel):
    id: int | None = None
    title: str
    description: str