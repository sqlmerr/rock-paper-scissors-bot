from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="find", description="Find game"),
        BotCommand(command="profile", description="Your profile"),
    ]

    return await bot.set_my_commands(
        commands,
        BotCommandScopeDefault()
    )
