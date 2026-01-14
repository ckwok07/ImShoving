from dataclasses import dataclass

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

    street:str
