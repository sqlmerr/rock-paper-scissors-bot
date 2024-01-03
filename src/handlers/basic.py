from loguru import logger

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.db import User, get_user
from src.utils import inline_builder
from src import version

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    if not await get_user(message.from_user.id):
        user = User(
            user_id=message.from_user.id
        )

        await user.insert()
        logger.debug(f"registered new user with id {message.from_user.id}")

    ver = ".".join(str(_) for _ in version)
    text = (
        f"✨ <b>Hello, {message.from_user.full_name}</b>.\n"
        "<i>I'm rock paper scissors game bot.</i>\n"
        f"My current version: <code>{ver}</code>"
    )

    await message.answer_sticker("CAACAgIAAxkBAAELFZtllXdIfkCn8voBjZtW2jmFjqIV9AAC8iwAAnDW4UuITBkIiCOD3zQE")
    await message.answer(
        text,
        reply_markup=inline_builder(["Search game", "search"])
    )
