# admin_api/app/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    publisher = Column(String, nullable=True)
    category = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)

    borrowings = relationship("Borrowing", back_populates="book")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    

    borrowings = relationship("Borrowing", back_populates="user")


class Borrowing(Base):
    __tablename__ = "borrowings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime)
    return_date = Column(DateTime)  

    user = relationship("User", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
