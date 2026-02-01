from controller.action import Action
from main.model.Card import Card
from main.model.Simulator import Simulator
from controller.gameState import GameState

class GTOModel:
    def __init__(self):
        pass
        
    def facing_bet(self, state: GameState, legal_actions: list[Action], equity: float) -> dict[Action, dict]:
        to_call = (state.current_bet - state.villain_amt)
        pot_odds = to_call / (state.pot + to_call)
        mdf = state.pot / (state.pot + to_call)

        fold_action = None
        call_action = None
        raise_actions = []
        result = {}

        for action in legal_actions:
            if action.name == "FOLD":
                fold_action = action
            elif action.name == "CALL":
                call_action = action
            elif action.name in ("RAISE", "ALL IN"):
                raise_actions.append(action)

        if equity < pot_odds - 0.15: # very weak hand
            fold_freq = 0.85
            call_freq = 0.10
            raise_freq = 0.05 
        elif equity < pot_odds: # weak hand
            fold_freq = 0.65
            call_freq = 0.25
            raise_freq = 0.10
        elif equity < pot_odds + 0.15: # solid hand
            fold_freq = max(0.10, 1 - mdf)
            call_freq = 0.60
            raise_freq = 0.30
        else: # strong hand
            fold_freq = 0.05
            call_freq = 0.45
            raise_freq = 0.50

        if fold_action:
            result[fold_action] = {"frequency": fold_freq,
                                   "ev": 0}
        
        if call_action:
            result[call_action] = {"frequency": call_freq,
                                   "ev": (equity * (state.pot + to_call)) - to_call}
            
        if raise_actions:
            freq = raise_freq / len(raise_actions)
            for raise_action in raise_actions:
                raise_cost = raise_action.size - state.villain_amt
                final_pot = state.pot + 2 * raise_cost
                ev = equity * final_pot - raise_cost

                result[raise_action] = {"frequency" : freq,
                                        "ev": ev}


        return result




    def first_to_act(self, state: GameState, legal_actions: list[Action], equity: float) -> dict:
        pass

    def facing_check(self, state: GameState, legal_actions: list[Action], equity: float) -> dict:
        pass