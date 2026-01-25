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

    hero_action_count: int = 0
    hero_check_count: int = 0
    hero_fold_count: int = 0
    hero_call_count: int = 0
    hero_raise_count: int = 0
    hero_bet_count: int = 0

    villain_action_count: int = 0
    villain_check_count: int = 0
    villain_fold_count: int = 0
    villain_call_count: int = 0
    villain_raise_count: int = 0
    villain_bet_count: int = 0

    hand_over: bool = False
    animating: bool = False
