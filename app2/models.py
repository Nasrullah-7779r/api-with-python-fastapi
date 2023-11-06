from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .DB import Base


class Note(Base):
    __tablename__ = "Note"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("User.id", ondelete="cascade"), nullable=False)
    user = relationship("User")


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Like(Base):
    __tablename__ = "Like"

    user_id = Column(Integer, ForeignKey("User.id", ondelete="cascade"), primary_key=True)
    note_id = Column(Integer, ForeignKey("Note.id", ondelete="cascade"), primary_key=True)
