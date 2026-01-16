from dataclasses import dataclass
from typing import Optional

from main.model.Card import Card

@dataclass
class Action:
    name: str
    player: str
    size: float
    ev: float | None = None
    cards: list[Card] | None = None
    cards2: list[Card] | None = None
    pot_after = 0