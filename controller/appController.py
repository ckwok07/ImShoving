from .gameState import GameState
from .action import Action

class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
    
    def handle_action(self, action: Action) -> None:
        print("state before:", self.state)

        if action.name == "CHECK":
            pass

        elif action.name == "CALL":
            pass

        elif action.name == "RAISE" and action.size is not None:
            self.state.pot *= action.size

        elif action.name == "ALL_IN":
            print("ALL IN clicked")

        print("state after:", self.state)