from dataclasses import dataclass, field
from typing import List, Optional

from controller.action import Action

STREETS = ["PREFLOP", "FLOP", "TURN", "RIVER", "SHOWDOWN"]

@dataclass
class GameState:
    street: str
    board: List[str]
    pot:float
    hero_hand: Optional[List[str]] = None
    actions: List[Action] = field(default_factory=list)
