from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, BigInteger, Enum  # Добавляем Enum в импорт
from .db import Base
from datetime import datetime
from sqlalchemy.orm import relationship
import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"

# Ассоциативная таблица для связи многие-ко-многим между пользователями и диалогами
user_dialogue_association = Table(
    'user_dialogue',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('dialogue_id', Integer, ForeignKey('dialogues.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(UserRole),  # Теперь Enum импортирован
                  default=UserRole.USER, 
                  nullable=False)
    
    # Связи
    sent_messages = relationship('Message', back_populates='sender')
    dialogues = relationship(
        'Dialogue',
        secondary=user_dialogue_association,
        back_populates='participants'
    )

class Dialogue(Base):
    __tablename__ = 'dialogues'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    participants = relationship(
        'User',
        secondary=user_dialogue_association,
        back_populates='dialogues'
    )
    messages = relationship('Message', back_populates='dialogue')

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Внешние ключи
    sender_id = Column(Integer, ForeignKey('users.id'))
    dialogue_id = Column(Integer, ForeignKey('dialogues.id'))
    
    # Связи
    sender = relationship('User', back_populates='sent_messages')
    dialogue = relationship('Dialogue', back_populates='messages')

