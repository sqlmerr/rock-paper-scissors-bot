from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.db import User, get_user

router = Router()


@router.message(Command("profile"))
async def profile_cmd(message: Message, user: User):
    text = (
        "❇️ <b><i>Your profile:</i></b>\n\n"
        f"<b>Games played:</b> <code>{user.wins + user.loses}</code>\n"
        f"<b>Wins:</b> <code>{user.wins}</code>\n"
        f"<b>Loses:</b> <code>{user.loses}</code>\n\n"
        f"<b>Register date:</b> {user.register_date.strftime('%d/%m/%Y, %H:%M:%S')}"
    )

    await message.answer_sticker("CAACAgIAAxkBAAELFjpllbioO_ozhAnDeI38Yjh3wJOHPwACLjAAAi5d4EviHZzzZhcBGDQE")
    await message.answer(text)
