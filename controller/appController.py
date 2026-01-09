from main.model.Deck import Deck
from .gameState import GameState, STREETS
from .action import Action


class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
        self.deck = Deck()
        self.state_change = None
    
    def handle_action(self, action: Action) -> None:
        self.state.actions.append(action)
        print(self.state.actions)

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