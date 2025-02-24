"""Init-Module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base


DB_URL = "sqlite:///project_tracker.db"

engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
