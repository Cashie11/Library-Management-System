from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db
from .models import User, Book
from .schemas import UserCreate, BookOut, BorrowRequest
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Frontend API"}

@router.post("/users/enroll", response_model=UserCreate)
def enroll_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already enrolled")
    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/books", response_model=List[BookOut])
def list_books(
    publisher: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Book).filter(Book.is_available == True)
    if publisher:
        query = query.filter(Book.publisher == publisher)
    if category:
        query = query.filter(Book.category == category)
    books = query.all()
    return books

@router.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books/{book_id}/borrow")
def borrow_book(book_id: int, borrow: BorrowRequest, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")
    
    book.is_available = False
    db.commit()
    db.refresh(book)
    
    return_date = datetime.utcnow() + timedelta(days=borrow.duration)
    return {"message": "Book borrowed successfully", "return_date": return_date.isoformat()}
