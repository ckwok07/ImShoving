from controller.gameState import GameState
from controller.action import Action
from .Analyzer import Analyzer
from .DecisionChooser import DecisionChooser

class Villain:
    def __init__(self) -> None:
        self.analyzer = Analyzer()
        self.decisionChooser = DecisionChooser()

    def choose_action(self, state: GameState) -> Action:
        pass

    def observe_hero(self, state: GameState) -> None:
        self.analyzer.update_tree(state)



