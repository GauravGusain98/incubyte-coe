from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from sqlalchemy import Column, DateTime, func

engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
