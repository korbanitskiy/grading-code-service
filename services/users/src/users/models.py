from sqlalchemy import Column, Integer, Boolean, String

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    is_active = Column(Boolean, nullable=False, default=True)
