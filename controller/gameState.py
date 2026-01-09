from dataclasses import dataclass, field
from typing import List, Optional

from controller.action import Action

STREETS = ["PREFLOP", "FLOP", "TURN", "RIVER", "SHOWDOWN"]

@dataclass
class GameState:
    street: str
    board: List[str]
    pot:float

    current_bet: float
    hero_amt: float
    villain_amt: float

    hero_hand: Optional[List[str]] = None
    villain_hand: Optional[List[str]] = None
    actions: List[Action] = field(default_factory=list)

    hero_all_in: bool = False
    villain_all_in: bool = False

    hero_stack: int = 100
    villain_stack: int = 100

    hand_over: bool = False
