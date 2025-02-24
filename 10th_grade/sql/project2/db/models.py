"""Module provides tables class"""
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, Table, UniqueConstraint
)

Base = declarative_base()

association_table = Table(
    "association", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("project_id", Integer, ForeignKey("projects.id")),
    UniqueConstraint("user_id", "project_id", name="unique_id_pairs")
)


class User(Base):
    """
    Class represents users table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    profile = relationship("Profile", backref="user", uselist=False)

    projects = relationship(
        "Project",
        secondary=association_table,
        back_populates="users"
    )

    def __str__(self) -> str:
        return f"id: {self.id} | username: {self.username} | email: {self.email}"

    def __repr__(self) -> str:
        return str(self)


class Profile(Base):
    """
    Class represents profiles table
    """
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    bio = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"),
                     nullable=False, unique=True)

    def __str__(self) -> str:
        return f"id: {self.user.id} | "\
               f"username: {self.user.username} | "\
               f"email: {self.user.email} | "\
               f"phone: {self.phone}"

    def __repr__(self) -> str:
        return str(self)


class Project(Base):
    """
    Class represents projects table
    """
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="projects"
    )

    def __str__(self) -> str:
        return f"id: {self.id} | title: {self.title}"

    def __rept__(self) -> str:
        return str(self)


class Task(Base):
    """
    Class represents tasks table
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    status = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", backref="tasks", uselist=False)

    def __str__(self) -> str:
        return f"id: {self.id} | title: {self.title} | status: {self.status}"

    def __rept__(self) -> str:
        return str(self)
