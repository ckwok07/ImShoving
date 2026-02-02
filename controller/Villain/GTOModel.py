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
            result[(fold_action.name, fold_action.size)] = {"frequency": fold_freq,
                                                            "ev": 0}
        
        if call_action:
            result[(call_action.name, call_action.size)] = {"frequency": call_freq,
                                                            "ev": (equity * (state.pot + to_call)) - to_call}
            
        if raise_actions:
            freq = raise_freq / len(raise_actions)
            for raise_action in raise_actions:
                raise_cost = raise_action.size - state.villain_amt
                final_pot = state.pot + 2 * raise_cost
                ev = equity * final_pot - raise_cost

                result[(raise_action.name, raise_action.size)] = {"frequency" : freq,
                                                                  "ev": ev}


        return result

    # hero_prob responding to a first action by villain
    def first_to_act(self, state: GameState, legal_actions: list[Action], equity: float, hero_probs: dict[str, float] | None = None) -> dict:
        check_action = None
        bet_actions = []
        result = {}

        for action in legal_actions:
            if action.name == "CHECK":
                check_action = action
            elif action.name in ("BET", "ALL IN"):
                bet_actions.append(action)
        
        if not bet_actions:
            if check_action:
                return {check_action: {"frequency": 1.0, "ev": equity * state.pot}}
            return {}

        if equity < 0.25:  # very weak hands
            check_freq = 0.70
            bet_freq = 0.30
        elif equity < 0.45:  # weak hands
            check_freq = 0.85
            bet_freq = 0.15
        elif equity < 0.65:  # solid hands
            check_freq = 0.90
            bet_freq = 0.10
        elif equity < 0.80:  # strong hands
            check_freq = 0.40
            bet_freq = 0.60
        else:  # very strong hands
            check_freq = 0.20
            bet_freq = 0.80

        if check_action:
            result[check_action] = {"frequency": check_freq,
                                    "ev": equity * state.pot}
        
        if bet_actions:
            freq = bet_freq / len(bet_actions)
            for bet_action in bet_actions:
                bet_size = bet_action.size - state.villain_amt

                if hero_probs and "FOLD" in hero_probs:
                    fold_prob = hero_probs["FOLD"]
                else:
                    bet_to_pot_ratio = bet_size / state.pot if state.pot > 0 else 1.0
                    fold_prob = min(0.7, 0.2 + 0.3 * bet_to_pot_ratio)
                
                final_pot = state.pot + 2 * bet_size
                ev = (fold_prob * state.pot) + ((1 - fold_prob) * (equity * final_pot - bet_size))
                
                result[bet_action] = {"frequency": freq, 
                                      "ev": ev}
        return result
    
    # hero_prob responding to a bet by the villain after a check.
    def facing_check(self, state: GameState, legal_actions: list[Action], equity: float, hero_probs: dict[str, float] | None = None) -> dict:
        check_action = None
        bet_actions = []
        result = {}

        for action in legal_actions:
            if action.name == "CHECK":
                check_action = action
            elif action.name in ("BET", "ALL IN"):
                bet_actions.append(action)
        
        if not bet_actions:
            if check_action:
                return {check_action: {"frequency": 1.0, "ev": equity * state.pot}}
            return {}

        if equity < 0.25:  # very weak hands
            check_freq = 0.65
            bet_freq = 0.35
        elif equity < 0.45:  # weak hands
            check_freq = 0.60
            bet_freq = 0.40
        elif equity < 0.65:  # solid hands
            check_freq = 0.80
            bet_freq = 0.20
        elif equity < 0.80:  # strong hands
            check_freq = 0.45
            bet_freq = 0.55
        else:  # very strong hands
            check_freq = 0.30
            bet_freq = 0.70

        if check_action:
            result[check_action] = {"frequency": check_freq,
                                    "ev": equity * state.pot}
        
        if bet_actions:
            freq = bet_freq / len(bet_actions)
            for bet_action in bet_actions:
                bet_size = bet_action.size - state.villain_amt

                if hero_probs and "FOLD" in hero_probs:
                    fold_prob = hero_probs["FOLD"]
                else:
                    bet_to_pot_ratio = bet_size / state.pot if state.pot > 0 else 1.0
                    fold_prob = min(0.7, 0.2 + 0.3 * bet_to_pot_ratio)
                
                final_pot = state.pot + 2 * bet_size
                ev = (fold_prob * state.pot) + ((1 - fold_prob) * (equity * final_pot - bet_size))
                
                result[bet_action] = {"frequency": freq, 
                                      "ev": ev}
        return result