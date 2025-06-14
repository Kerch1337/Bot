import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from utils.logger import logger

load_dotenv('.env', encoding='utf-8')

Base = declarative_base()
DATABASE_URL = os.getenv("DB_URL")  # Пример: postgresql+asyncpg://user:pass@host:port/db

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    """Создание таблиц"""
    from .model import User, Dialogue, Message  # обязательно импортировать модели
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("База данных инициализирована")

def get_session():
    return async_session
