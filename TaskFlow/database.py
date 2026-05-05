from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, Session,declarative_base
Base = declarative_base()


DATABASE_URL = "postgresql://postgres:password123@localhost:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    echo=True,        # prints SQL queries for debugging
    future=True       # use 2.x style API
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=Session
)

def get_db():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))  # optional health check
        yield db
    finally:
        db.close()
        
        
