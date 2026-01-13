from dataclasses import dataclass
from typing import Optional

@dataclass
class Action:
    name: str
    player: str
    size: float
    ev: float | None = None
    pot_after = 0