from dataclasses import dataclass
from typing import Optional

@dataclass
class Action:
    name: str
    player: str
    size: Optional[float] = None
    ev: float | None = None