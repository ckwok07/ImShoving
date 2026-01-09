from main.model.Deck import Deck
from .gameState import GameState, STREETS
from .action import Action


class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
        self.deck = Deck()
        self.state_change = None
    
    def handle_action(self, action: Action) -> None:
        self.apply_action(action)

        self.state.actions.append(action)

        if self.round_complete():
            self.advance_street()

        if self.state_change:
            self.state_change(self.state)

    def advance_street(self) -> None:
        current = self.state.street
        index = STREETS.index(current)

        if index >= len(STREETS) - 1:
            return
        
        nxt = STREETS[index+1]
        self.state.street = nxt

        if nxt == "FLOP":
            self.state.board.extend(self.deck.draw(3))
        elif nxt == "TURN" or nxt == "RIVER":
            self.state.board.extend(self.deck.draw(1))

    def round_complete(self) -> bool:
        return True
    
    def apply_action(self, action: Action) -> None:
        if action.name == "CHECK":
            self.apply_check()

        elif action.name == "CALL":
            self.apply_call()

        elif action.name == "RAISE" and action.size is not None:
            self.apply_raise(action.size)

        elif action.name == "ALL_IN":
            self.apply_all_in()

    def apply_check(self) -> None:
        return None

    def apply_call(self) -> None:
        return None
    
    def apply_raise(self, size: float) -> None:
        return None
    
    def apply_all_in(self) -> None:
        self.state.hero_all_in = True
    
