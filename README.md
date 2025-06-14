# Telegram Bot на aiogram 3.x с Docker

Простой Telegram-бот с обработкой команд и текстовых сообщений, интеграцией с openAI и PostgreSQL.

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
├── .dockerignore                       # Исключения для Docker-контекста
├── .gitattributes                      # Настройки Git для работы с файлами
├── .gitignore                          # Исключения для Git
├── docker-compose.yml                  # Конфигурация docker-compose для запуска всех сервисов
├── alembic.ini                         # Конфигурация Alembic для миграций базы данных
├── Dockerfile                          # Docker-образ для основного приложения
├── Dockerfile.alembic                  # Docker-образ для выполнения миграций
├── README.md                           # Документация проекта
├── requirements.txt                    # Список зависимостей Python
├── app/                                # Основная директория приложения
│   ├── main.py                         # Точка входа в приложение
│   ├── database/                       # Работа с базой данных
│   │   ├── db.py                       # Подключение к БД и создание сессий
│   │   └── model.py                    # SQLAlchemy-модели
│   ├── handlers/                       # Обработчики команд и сообщений 
│   │   ├── commands.py                 # Обработка команд
│   │   └── messages.py                 # Обработка обычных текстовых сообщений
│   ├── images/                         # Хранение статичных изображений
│   │   └── okak.jpg                    # Картинка "окак"
│   ├── middlewares/                    # middleware-компоненты
│   │   └── middleware.py               # middleware
│   ├── keyboards/                      # Кастомные клавиатуры Telegram
│   │   └── reply.py                    # Реализация reply-клавиатуры
│   ├── services/                       # Сервисы внешних API
│   │   └── openai_client.py            # Работа с OpenAI API
│   └── utils/                          # Вспомогательные утилиты
│       └── logger.py                   # Конфигурация логирования
└── migrations/                         # Миграции базы данных (генерируются Alembic) 
    ├── version/                        # Сами версии миграций
    ├── env.py                          # Логика генерации и применения миграций
    ├── README                          # Описание схемы миграций
    └── script.py.mako                  # Шаблон для новых миграций
</pre>

## Создать файл .env в корне проекта:

DB_URL=postgresql+asyncpg://user:password@host:port/name_base  
BOT_TOKEN=ваш_токен_бота  
POSTGRES_DB=mydatabase  
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=qwerty123  
DB_HOST=db  
DB_PORT=5432  
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

## Посмотреть логи контейнера:
docker logs telegram_bot