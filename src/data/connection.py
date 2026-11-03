from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(settings.DATABASE_URL,connect_args={"check_same_thread":False})
# engine : connecting to the DB : btw python app and the db
# session : use the engine, to send the queries

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
        
    finally:
        db.close()