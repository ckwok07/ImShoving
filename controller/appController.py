from main.model.Deck import Deck
from .gameState import GameState, STREETS
from .action import Action


class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
        self.deck = Deck()
        self.deck.shuffle()
        self.state.hero_hand = self.deck.deal(2)
        self.state_change = None
    
    def handle_action(self, action: Action) -> None:
        if self.state.hand_over:
            return
        self.apply_action(action)

        self.state.actions.append(action)

        print(f"ACTION={action.name}, "
              f"current_bet={self.state.current_bet}, "
              f"hero_amt={self.state.hero_amt}, "
              f"pot={self.state.pot},"
              f"board = {self.state.board}")

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
            self.state.board.extend(self.deck.deal(3))
        elif nxt == "TURN" or nxt == "RIVER":
            self.state.board.extend(self.deck.deal(1))

    def round_complete(self) -> bool:
        return True
    
    def apply_action(self, action: Action) -> None:
        if action.name == "FOLD":
            self.apply_fold()
            return
        
        if action.name == "CHECK":
            self.apply_check()

        elif action.name == "CALL":
            self.apply_call()

        elif action.name == "RAISE" and action.size is not None:
            self.apply_raise(action.size)

        elif action.name == "ALL_IN":
            self.apply_all_in()

    def apply_check(self) -> None:
        return

    def apply_call(self) -> None:
        amount = self.state.current_bet - self.state.hero_amt

        if amount <= 0:
            return

        self.state.hero_amt += amount
        self.state.pot += amount
    
    def apply_raise(self, size: float) -> None:
        if self.state.current_bet == 0:
            new_bet = size
        else:
            new_bet = self.state.current_bet * size

        raise_amt = new_bet - self.state.hero_amt
        if raise_amt <= 0:
            return

        self.state.current_bet = new_bet
        self.state.hero_amt += raise_amt
        self.state.pot += raise_amt
    
    def apply_all_in(self) -> None:
        self.state.hero_all_in = True
    
    def apply_fold(self) -> None:
        self.state.hand_over = True
        self.state.street = "SHOWDOWN"

    def new_hand(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()
        self.state.hero_hand = self.deck.deal(2)

        self.state.street = "PREFLOP"
        self.state.board.clear()

        self.state.current_bet = 0
        self.state.hero_amt = 0
        self.state.villain_amt = 0

        self.state.actions.clear()

        if self.state_change:
            self.state_change(self.state)
    
