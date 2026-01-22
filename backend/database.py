from sqlalchemy import create_engine
from .config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database engine
engine = create_engine(settings.DATABASE_URL)

# sessionmaker is a class that helps us create a 'SessionLocal' class
# autocommit=False: We want to manually decide when to save data
# autoflush=False: We don't want it to send data to the DB until we are ready
# bind=engine: This tells the factory which 'pipe' (engine) to use
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        # Start a session with the caller
        yield db
    finally:
        # Close current session after API request is done
        db.close()