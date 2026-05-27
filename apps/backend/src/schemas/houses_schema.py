from pydantic import BaseModel

class HousesSchema(BaseModel):
    id: int | None = None
    title: str
    description: str