from aiogram import Router
from . import basic, search


def register_routers() -> Router:
    router = Router()

    router.include_routers(
        basic.router,
        search.router,
        search.playing.router,
    )

    return router
