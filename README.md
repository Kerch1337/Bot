# Telegram Bot на aiogram 3.x с Docker

Простой Telegram-бот с обработкой команд, текстовых сообщений и интеграцией с PostgreSQL.

## Функционал
- Обработка команды `/start`
- Ответы на текстовые сообщения:
  - `привет` - приветствие
  - `помощь` - список команд
  - `мои данные` - информация о пользователе
  - `окак` - отправка изображения
  - Любой другой текст - переворачивает строку
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
├── Dockerfile
├── README.md
├── requirements.txt
└── app/
    ├── bot.py
    ├── main.py
    ├── database/
    │   ├── db.py
    │   └── model.py
    ├── handlers/
    │   ├── commands.py
    │   └── messages.py
    ├── images/
    │   └── okak.jpg
    ├── keyboards/
    │   └── reply.py
    └── utils/
        └── logger.py
</pre>

## Создать файл .env в корне проекта:

BOT_TOKEN=ваш_токен_бота  
DB_USER=postgres  
DB_PASSWORD=postgres_password  
DB_HOST=db  
DB_PORT=5432  
DB_NAME=bot_db  

## Собрать и запустить контейнеры с проектом:

docker-compose build --no-cache  
docker-compose up -d