import asyncio
import random

from loguru import logger
from typing import Union

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from src.db import User, Game
from src.utils import inline_builder, PlayerStatus
from . import playing

router = Router()


@router.message(Command("find"))
@router.callback_query(F.data == "search")
async def search_game(event: Union[CallbackQuery, Message], user: User):
    if user.status != PlayerStatus.nothing:
        text = "<b>You're already searching or playing a game.</b>\n<i>Do you want to leave the game or search?</i>"
        if isinstance(event, CallbackQuery):
            await event.message.answer(text, reply_markup=inline_builder(["leave", "leave"]))
        else:
            await event.answer(text, reply_markup=inline_builder(["leave", "leave"]))
        return

    await event.answer("Seacrhing game...")
    user.status = PlayerStatus.searching
    await user.save()

    players = await User.find_many(User.status == PlayerStatus.searching, User.user_id != user.user_id).to_list()
    if not players:
        return

    if players:
        await asyncio.sleep(1)
        opponent = random.choice(players)
        game = Game(
            players=[user, opponent],
            score=[0, 0]
        )
        await game.insert()

        for p in game.players:
            p: User
            p.status = PlayerStatus.playing
            p.current_game = game.id
            await event.bot.send_message(p.user_id, "Found a game!")

            await p.save()

        await playing.playing_game(event.bot, game)


@router.callback_query(F.data == "leave")
async def leave_game(call: CallbackQuery, user: User):
    if user.status == PlayerStatus.nothing:
        await call.answer()
        return

    if user.current_game:
        game = await Game.get(user.current_game, fetch_links=True)

        opponent = [_ for _ in game.players if _.user_id != user.user_id][0]
        opponent.status = PlayerStatus.nothing
        opponent.current_game = None
        await opponent.save()
        await call.bot.send_message(opponent.user_id, "Your opponent left the game")

        await game.delete()
        await call.answer("You have successfully left the game")
    else:
        await call.answer("You have successfully left the search")

    user.status = PlayerStatus.nothing
    user.current_game = None
    await user.save()

