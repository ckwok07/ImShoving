from dataclasses import dataclass, field
from typing import List, Optional
from main.model.Card import Card

from controller.action import Action

STREETS = ["PREFLOP", "FLOP", "TURN", "RIVER", "SHOWDOWN"]

@dataclass
class GameState:
    street: str
    board: List[Card]
    pot:float

    current_bet: float
    hero_amt: float
    villain_amt: float

    hero_hand: Optional[List[Card]] = None
    villain_hand: Optional[List[Card]] = None
    actions: List[Action] = field(default_factory=list)
    actions_list: List[Action] = field(default_factory=list)

    hero_all_in: bool = False
    villain_all_in: bool = False

    hero_stack: int = 100
    villain_stack: int = 100

    button_index: int = 0 #0 for player, 1 for villain
    to_act_index: int = 1

    hand_over: bool = False
    animating: bool = False
