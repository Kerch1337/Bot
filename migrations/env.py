from logging.config import fileConfig
import asyncio
import os
import sys
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool
from alembic import context

# Настройка путей, чтобы можно было импортировать модули
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

# Импорты моделей и базы
from database.db import DATABASE_URL
from database.model import * 
from database.db import Base

# Alembic config
config = context.config

# Логгинг
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Установка URL напрямую
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Метаданные моделей для автогенерации
target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск миграций в офлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True  # <-- сравнение типов колонок
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable: AsyncEngine = create_async_engine(
        DATABASE_URL,
        poolclass=NullPool,
    )

    async with connectable.connect() as connection:
        def do_migrations(sync_connection):
            context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
