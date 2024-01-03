from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.db import get_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Union[CallbackQuery, Message], Dict[str, Any]], Awaitable[Any]],
            event: Union[CallbackQuery, Message],
            data: Dict[str, Any],
    ) -> Any:
        user = await get_user(event.from_user.id)
        data["user"] = user

        return await handler(event, data)
