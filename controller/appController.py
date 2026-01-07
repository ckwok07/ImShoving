from .gameState import GameState
from .action import Action

class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
    
    def handle_action(self, action: Action) -> None:
        print(f"state = {self.state}")
        print(f"action = {action}")