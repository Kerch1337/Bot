from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    full_name = Column(String)