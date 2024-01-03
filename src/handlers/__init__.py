from aiogram import Router
from . import basic, game


def register_routers() -> Router:
    router = Router()

    router.include_routers(
        basic.router,
        game.router
    )

    return router
