import asyncio
import random
from loguru import logger

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from src.db import User, Game
from src.utils import inline_builder, PlayerStatus

router = Router()


@router.callback_query(F.data == "search")
async def search_game(call: CallbackQuery, user: User):
    if user.status != PlayerStatus.nothing:
        await call.answer()
        return

    await call.answer("Seacrhing game...")
    user.status = PlayerStatus.searching
    await user.save()

    while True:
        players = await User.find_many(User.status == PlayerStatus.searching, User.user_id != user.user_id).to_list()
        if players:
            await asyncio.sleep(1)
            game = Game(
                players=[user, random.choice(players)],
                score=[0, 0]
            )
            await game.insert()

            text = "Found a game!"

            for player in game.players:
                await call.bot.send_message(player.user_id, text)

            first = random.choice(game.players)
            await call.bot.send_message(first.user_id, "hi")

            return

        await asyncio.sleep(3)
