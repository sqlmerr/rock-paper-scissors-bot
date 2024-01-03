from datetime import datetime
from typing import List, Optional, Dict

from beanie import Document, Indexed, Link, PydanticObjectId
from src.utils import PlayerStatus


class User(Document):
    user_id: Indexed(int, unique=True)
    register_date: datetime

    wins: int = 0
    loses: int = 0

    status: PlayerStatus = PlayerStatus.nothing
    current_game: Optional[PydanticObjectId] = None


class Game(Document):
    players: List[Link[User]]
    score: List[int]

    rounds: int = 0
    current_round: Optional[Dict] = {}
