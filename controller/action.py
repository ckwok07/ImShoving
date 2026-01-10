from dataclasses import dataclass
from typing import Optional

@dataclass
class Action:
    name: str
    size: Optional[float] = None