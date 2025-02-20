from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .database import get_db
from .models import Book, User, Borrowing
from .messaging import publish_book_update
from pydantic import BaseModel

router = APIRouter()

class BookCreate(BaseModel):
    title: str
    publisher: Optional[str] = None
    category: Optional[str] = None

    class Config:
        orm_mode = True

class BookOut(BaseModel):
    id: int
    title: str
    publisher: Optional[str] = None
    category: Optional[str] = None
    is_available: bool

    class Config:
        orm_mode = True

@router.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(
        title=book.title,
        publisher=book.publisher,
        category=book.category,
        is_available=True,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    

    book_data = {
        "id": new_book.id,
        "title": new_book.title,
        "publisher": new_book.publisher,
        "category": new_book.category,
        "is_available": new_book.is_available,
    }
    publish_book_update({"action": "add", "book": book_data})
    return new_book

@router.delete("/books/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    publish_book_update({"action": "remove", "book_id": book_id})
    return {"message": "Book removed successfully"}


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


class BorrowingOut(BaseModel):
    book: BookOut
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserBorrowedOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    borrowings: List[BorrowingOut] = []

    class Config:
        orm_mode = True

@router.get("/borrowed", response_model=List[UserBorrowedOut])
def list_users_with_borrowings(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

class UnavailableBookOut(BaseModel):
    id: int
    title: str
    publisher: Optional[str] = None
    category: Optional[str] = None
    expected_return_date: Optional[str] = None

    class Config:
        orm_mode = True

@router.get("/books/unavailable", response_model=List[UnavailableBookOut])
def list_unavailable_books(db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.is_available == False).all()
    result = []
    for book in books:

        borrowing = book.borrowings[0] if hasattr(book, "borrowings") and book.borrowings else None
        result.append({
            "id": book.id,
            "title": book.title,
            "publisher": book.publisher,
            "category": book.category,
            "expected_return_date": borrowing.return_date.isoformat() if borrowing and borrowing.return_date else None
        })
    return result
