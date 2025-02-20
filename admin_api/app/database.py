from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


# Use a separate database URL for the Admin API
DATABASE_URL = "sqlite:///./admin.db"

# Create the SQLAlchemy engine.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
