from controller.gameState import GameState
from controller.action import Action
from .Analyzer import Analyzer

class DecisionChooser:
    def __init__(self):
        pass

    def get_villain_legal_actions(self, state: GameState) -> list[Action]:
        pass

    def compute_villain_equity(self, state: GameState) -> float:
        pass

    def compute_action_EVs(self, actions: list[Action], analyzer: Analyzer) -> list[Action]:
        pass

    def get_best_action(self, actions: list[Action]):
        pass