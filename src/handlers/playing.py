import asyncio
import random
from typing import Union, Dict

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from src.db import User, Game
from src.utils import inline_builder, PlayerStatus

router = Router()

emojis = {
    "rock": "🪨",
    "paper": "📃",
    "scissors": "✂️"
}

async def playing_game(bot: Bot, game: Game):
    for player in game.players:
        await bot.send_message(
            player.user_id,
            "<i><b>Please choose rock, paper or scissors</b></i>",
            reply_markup=inline_builder(
                ["🪨", "rock"],
                ["📃", "paper"],
                ["✂️", "scissors"],
                per_row=[3]
            )
        )


@router.callback_query(F.data.in_(["rock", "paper", "scissors"]))
async def chosen_call(call: CallbackQuery, user: User):
    async def send_txt(game: Game):
        text = ""
        for index, player in enumerate(game.players):
            chat = await call.bot.get_chat(player.user_id)
            text += f"{chat.first_name} - {emojis[game.current_round[str(player.user_id)]]} - {game.score[index]}\n"
        # text += f"\n<i>{}</i>"
        for player in game.players:
            await call.bot.send_message(player.user_id, text)
        return text

    game = await Game.get(user.current_game, fetch_links=True)
    if not game:
        await call.answer()
        return

    if str(user.user_id) in game.current_round.keys():
        await call.answer()
        return

    if game.rounds >= 3:
        winner = await calculate_winner(game)
        winner.wins += 1
        await winner.save()
        for player in game.players:
            text = "You lose!"
            if player.user_id == winner.user_id:
                text = "You won!"
            await call.bot.send_message(
                player.user_id,
                text
            )
            player.status = PlayerStatus.nothing
            await player.save()
        await game.delete()
        return

    game.current_round[str(user.user_id)] = call.data

    await call.answer(f"You chose {call.data}")
    await game.save()
    if len(game.current_round.keys()) == 2:
        round_winner = await calculate_round_winner(game.current_round, game)
        if round_winner is False:
            await send_txt(game)
            game.current_round = {}
            await game.save()
            await playing_game(call.bot, game)
            return

        await call.bot.send_message(round_winner, "You won this round")
        for index, player in enumerate(game.players):
            if player.user_id == int(round_winner):
                game.score[index] += 1
                await game.save()
        game.rounds += 1
        await send_txt(game)
        game.current_round = {}
        await game.save()
        await playing_game(call.bot, game)


async def calculate_round_winner(r: Dict, game: Game) -> Union[int, bool]:
    rvalues = list(r.values())

    if rvalues[0] == rvalues[1]:
        return False

    if rvalues == ['rock', 'paper'] or rvalues == ['paper', 'rock']:
        return int([k for k, v in r.items() if v == 'paper'][0])

    if rvalues == ['rock', 'scissors'] or rvalues == ['scissors', 'rock']:
        return int([k for k, v in r.items() if v == 'rock'][0])

    if rvalues == ['scissors', 'paper'] or rvalues == ['paper', 'scissors']:
        return int([k for k, v in r.items() if v == 'scissors'][0])


async def calculate_winner(game: Game) -> User:
    max_score = max(game.score)
    return game.players[game.score.index(max_score)]
