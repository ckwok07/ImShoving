from .gameState import GameState

class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state