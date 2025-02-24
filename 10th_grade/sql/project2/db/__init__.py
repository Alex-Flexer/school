"""Init-Module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Status


DB_URL = "sqlite:///project_tracker.db"

STATUSES = ['N', 'P', 'R', 'T', 'D']
# N - New
# P - in Progress
# R - code Review
# T - Testing
# D - Done


def init_statuses():
    """Function inits statuses table if necessary"""
    with Session() as temp_session:
        cur_statuses = [status.status
                        for status in temp_session.query(Status).all()]

        if cur_statuses != STATUSES:
            temp_session.query(Status).delete()
            for status in STATUSES:
                temp_session.add(Status(status=status))
            temp_session.commit()


engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

init_statuses()
