from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Task, Profile, Profile, User


DB_URL = "sqlite:///tasks.db"

engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
