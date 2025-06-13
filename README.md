# Telegram Bot на aiogram 3.x с Docker

Простой Telegram-бот с обработкой команд, текстовых сообщений и интеграцией с PostgreSQL.

## Функционал
- Обработка команды `/start` - начать общение
- Обработка команды `/re_chat` - история сообщений
- Ответы на текстовые сообщения:
  - `привет` - приветствие
  - `помощь` - список команд
  - `мои данные` - информация о пользователе
  - `окак` - отправка изображения
  - Любой другой текст - отправляется в openAI и возвращается ответ
- Кастомная клавиатура
- Логирование в консоль
- Интеграция с PostgreSQL через SQLAlchemy

## Структура проекта

<pre>
Bot/
├── .dockerignore
├── .gitattributes
├── .gitignore
├── docker-compose.yml
├── alembic.ini
├── Dockerfile
├── Dockerfile.alembic
├── README.md
├── requirements.txt
├── app/
│   ├── main.py
│   ├── database/
│   │   ├── db.py
│   │   └── model.py
│   ├── handlers/
│   │   ├── commands.py
│   │   └── messages.py
│   ├── images/
│   │   └── okak.jpg
│   ├── middlewares/
│   │   └── middleware.py
│   ├── keyboards/
│   │   └── reply.py
│   └── utils/
│       └── logger.py
└── migrations/
    ├── version/
    ├── env.py
    ├── README
    └── script.py.mako
</pre>

## Создать файл .env в корне проекта:

DB_URL=postgresql://user:password@host:port/name_base
BOT_TOKEN=ваш_токен_бота  
DB_USER=postgres  
DB_PASSWORD=postgres_password  
DB_HOST=db  
DB_PORT=5432  
DB_NAME=bot_db
OPENAI_API_KEY=xxxx
PROXY_URL=http://login:password@ip:port

## Собрать и запустить контейнеры с проектом:

docker-compose build --no-cache  
docker-compose up -d

## Миграции:

Для создания миграции:  
docker-compose run --rm alembic alembic revision --autogenerate -m "Описание"

Для применения созданной миграции:  
docker-compose run --rm alembic alembic upgrade head

Для отката миграции:  
docker-compose run --rm alembic alembic downgrade -1

## Команда чтобы зайти в БД:
docker exec -it pg_db psql -U postgres -d mydatabase