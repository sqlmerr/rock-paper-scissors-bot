from aiogram import Router
from . import basic, search, profile


def register_routers() -> Router:
    router = Router()

    router.include_routers(
        basic.router,
        search.router,
        search.playing.router,
        profile.router,
    )

    return router
