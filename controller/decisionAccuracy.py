from dataclasses import dataclass

from main.model.Card import Card

ACCURACY_LABELS = {95: "Brilliant", 
                  85: "Excellent", 
                  70: "Good",
                  60: "Inaccuracy", 
                  40: "Mistake", 
                  0: "Blunder" }

@dataclass
class DecisionQuality:
    action_index: int
    action_name: str

    ev_chosen: float
    ev_best: float

    equity_before: float

    accuracy: float
    label: str

    hand: list[Card]
    board: list[Card]

    street:str
