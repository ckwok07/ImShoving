from controller.gameState import GameState
from controller.action import Action

class Analyzer:
    def __init__(self):
        self.hero_counts = {}

    def observe(self, state: GameState, villain_action_key: Action, hero_action:Action) -> None:
        pass

    def get_probabilities(self, state: GameState, villain_action_key: Action) -> list[float] | None:
        pass