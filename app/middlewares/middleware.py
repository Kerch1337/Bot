from aiogram import BaseMiddleware
from sqlalchemy.orm import sessionmaker
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        with self.session_pool() as session:
            data["session"] = session
            return handler(event, data)