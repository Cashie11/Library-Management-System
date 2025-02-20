# admin_api/app/schemas.py
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    publisher: str
    category: str

class BookOut(BaseModel):
    id: int
    title: str
    publisher: str
    category: str
    is_available: bool

    class Config:
        orm_mode = True
