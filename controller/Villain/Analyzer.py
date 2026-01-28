from controller.gameState import GameState
from controller.action import Action

class Analyzer:
    def __init__(self):
        pass

    def observe(self, state: GameState, hero_action:Action) -> None:
        pass

    def get_probabilities(self, state) -> list[float] | None:
        pass