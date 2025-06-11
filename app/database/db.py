import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from utils.logger import logger

# Инициализация базового класса для моделей
Base = declarative_base()
load_dotenv('.env', encoding='utf-8')
DATABASE_URL = os.getenv("DB_URL")

def init_db():
    """Инициализация подключения к БД с проверкой переменных окружения"""
    load_dotenv()
    
    # Получение параметров подключения
    db_config = {
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST"),
        'port': os.getenv("DB_PORT"),
        'name': os.getenv("DB_NAME")
    }
    
    global DATABASE_URL

    # Проверка конфигурации
    missing = [k for k, v in db_config.items() if not v]
    if missing:
        error_msg = f"Отсутствуют переменные окружения: {', '.join(missing)}"
        logger.critical(error_msg)
        raise EnvironmentError(error_msg)
    
    # Формирование DSN
    #DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
    logger.debug("Инициализация подключения к БД")
    
    # Создание движка и сессии
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine,
        expire_on_commit=False
    )
    
    return engine, SessionLocal

def get_db_session():
    """Фабрика сессий для использования в DI"""
    engine, SessionLocal = init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()