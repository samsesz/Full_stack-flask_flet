from pydantic import BaseModel

class DragonsSchema(BaseModel):
    id: int | None = None
    title: str
    description: str