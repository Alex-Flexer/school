from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column, Integer,
    String, ForeignKey, Table
)

Base = declarative_base()

association_table = Table(
    "association", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("project_id", Integer, ForeignKey("projects.id"))
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    projects = relationship(
        "Project",
        secondary=association_table,
        back_populates="users"
    )


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    bio = Column(String(255), nullable=False, unique=True)
    phone = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", backref="profile", uselist=False)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="projects"
    )


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", backref="tasks", uselist=False)
