from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column, Integer,
    String, ForeignKey, Table
)

Base = declarative_base()

association_table = Table(
    "association", Base.metadata,
    Column("user_id", Integer, ForeignKey("profiles.id"), unique=True),
    Column("project_id", Integer, ForeignKey("projects.id"), unique=True)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)

    def __str__(self) -> str:
        return f"id: {self.id} | username: {self.username} | email: {self.email}"

    def __repr__(self) -> str:
        return str(self)


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    bio = Column(String(255), nullable=False, unique=True)
    phone = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", backref="profile", uselist=False)

    projects = relationship(
        "Project",
        secondary=association_table,
        back_populates="users"
    )

    def __str__(self) -> str:
        return f"id: {self.user.id} | username: {self.user.username} | email: {self.user.email} | phone: {self.phone}"

    def __repr__(self) -> str:
        return str(self)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    users = relationship(
        "Profile",
        secondary=association_table,
        back_populates="projects"
    )

    def __str__(self) -> str:
        return f"id: {self.id} | title: {self.title}"

    def __rept__(self) -> str:
        return str(self)


class Task(Base):
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
