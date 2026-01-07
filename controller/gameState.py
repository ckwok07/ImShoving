from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GameState:
    street: str
    board: List[str]
    pot:float
    hero_hand: Optional[List[str]] = None
