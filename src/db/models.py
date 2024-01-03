from typing import List

from beanie import Document, Indexed, Link
from src.utils import PlayerStatus


class User(Document):
    user_id: Indexed(int, unique=True)
    wins: int = 0
    status: PlayerStatus = PlayerStatus.nothing


class Game(Document):
    players: List[Link[User]]
    score: List[int]

