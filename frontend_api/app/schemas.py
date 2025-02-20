from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    id: int
    title: str
    publisher: str
    category: str
    is_available: bool

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    publisher: str = None
    category: str = None

    class Config:
        orm_mode = True

class BorrowRequest(BaseModel):
    duration: int  

    class Config:
        orm_mode = True
