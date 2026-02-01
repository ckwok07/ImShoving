from controller.gameState import GameState
from controller.action import Action
from main.model.Simulator import Simulator
from main.model.Card import Card
from .Analyzer import Analyzer
from .GTOModel import GTOModel
import json
from pathlib import Path

class DecisionChooser:
    def __init__(self):
        self.gto_model = GTOModel()
        self.current_equity = None
        self.preflop_table = self.load_preflop_equity_table()

    def get_villain_decision(self, state: GameState):
        legal_actions = self.get_villain_legal_actions(state)

        equity = self.get_equity(state)

        gto_actions = self.get_gto_strategy(state, legal_actions, equity)

        return

    def get_villain_legal_actions(self, state: GameState) -> list[Action]:
        pass
    
    def get_gto_strategy(self, state: GameState, legal_actions: list[Action], equity: float) -> list[Action]:
        # facing bet or raise
        if state.current_bet > state.villain_amt: # facing bet
            return self.gto_model.facing_bet(state, legal_actions, equity)
            
        if state.street == "PREFLOP":
            villain_acts_first = bool(state.button_index == 1)
        else:
            villain_acts_first = bool(state.button_index == 0)

        # first to act
        if state.current_bet == 0 and state.villain_amt == 0 and villain_acts_first:
            return self.gto_model.first_to_act(state, legal_actions, equity)
        # facing a check
        else:
            return self.gto_model.facing_check(state, legal_actions, equity)

    def get_equity(self, state: GameState) -> float:
        if state.street == "PREFLOP":
            key = self.hand_to_key(state.villain_hand)
            return self.preflop_equity_table[key]["avg_equity"]

        else:
            return Simulator.simulate_equity(hand = state.villain_hand,
                                             board = state.board,
                                             players = 2,
                                             trials = 15000)
    
    def load_preflop_equity_table(self) -> None:
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        
        equity_file = project_root / 'data' / 'hand_equities_aggregated.json'

        with open(equity_file, 'r') as f:
            return json.load(f)
    
    def hand_to_key(self, hand: list[Card]):
        c1, c2 = hand

        if (c2.rank, c2.suit) > (c1.rank, c1.suit):
            c1, c2 = c2, c1

        hand1 = c1.display() + c2.display()

        if hand1[0] == hand1[2]:
            return f"{hand1[0]}{hand1[2]}"
        elif hand1[1] == hand1[3]: #suited
            return f"{hand1[0]}{hand1[2]}s"
        else:
            return f"{hand1[0]}{hand1[2]}o"