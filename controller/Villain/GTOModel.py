from controller.action import Action
from main.model.Card import Card
from main.model.Simulator import Simulator
from controller.gameState import GameState
import math

class GTOModel:
    def __init__(self):
        pass
        
    def facing_bet(self, state: GameState, legal_actions: list[Action], equity: float) -> dict[(str, float), dict]:
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
            fold_freq = 0.60
            call_freq = 0.30
            raise_freq = 0.10 
        elif equity < pot_odds: # weak hand
            fold_freq = 0.50
            call_freq = 0.35
            raise_freq = 0.15
        elif equity < pot_odds + 0.10: # solid hand
            fold_freq = max(0.10, 1 - mdf)
            call_freq = (1 - fold_freq) * .6
            raise_freq = (1 - fold_freq) * .4
        else: # strong hand
            fold_freq = 0.05
            call_freq = 0.55
            raise_freq = 0.40

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

                raise_in_pot_units = raise_cost / state.pot if state.pot > 0 else 1.0

                if raise_action.name == "ALL IN":
                    if raise_in_pot_units < 1.0:
                        hero_fold_prob = 0.35 + 0.30 * raise_in_pot_units
                    elif raise_in_pot_units < 3.0:
                        hero_fold_prob = 0.65 + 0.10 * (raise_in_pot_units - 1.0)
                    else:
                        hero_fold_prob = min(0.85, 0.75 + 0.03 * (raise_in_pot_units - 3.0))
                else:
                    hero_fold_prob = min(0.75, 0.25 + 0.25 * raise_in_pot_units)

                hero_call_prob = 1 - hero_fold_prob

                ev_hero_folds = hero_fold_prob * state.pot
                final_pot = state.pot + 2 * raise_cost
                ev_hero_calls = hero_call_prob * (equity * final_pot - raise_cost)
                
                ev = ev_hero_folds + ev_hero_calls

                result[(raise_action.name, raise_action.size)] = {"frequency": freq, "ev": ev}

        return result

    # hero_prob responding to a first action by villain
    def first_to_act(self, state: GameState, legal_actions: list[Action], equity: float, hero_probs: dict[str, float] | None = None) -> dict[(str, float), dict]:
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
                return {(check_action.name, check_action.size): {"frequency": 1.0, "ev": equity * state.pot}}
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
            result[(check_action.name, check_action.size)] = {"frequency": check_freq,
                                    "ev": equity * state.pot}
        
        if bet_actions:
            freq = bet_freq / len(bet_actions)
            for bet_action in bet_actions:
                bet_size = bet_action.size - state.villain_amt

                if hero_probs and "FOLD" in hero_probs:
                    fold_prob = hero_probs["FOLD"]
                else:
                    # FIXED: Add the same scaling logic as facing_bet
                    bet_in_pot_units = bet_size / state.pot if state.pot > 0 else 1.0
                    
                    if bet_action.name == "ALL IN":
                        if bet_in_pot_units < 1.0:
                            fold_prob = 0.35 + 0.30 * bet_in_pot_units
                        elif bet_in_pot_units < 3.0:
                            fold_prob = 0.65 + 0.10 * (bet_in_pot_units - 1.0)
                        else:
                            fold_prob = min(0.85, 0.75 + 0.03 * (bet_in_pot_units - 3.0))
                    else:
                        fold_prob = min(0.70, 0.20 + 0.25 * bet_in_pot_units)
                
                final_pot = state.pot + 2 * bet_size
                ev = (fold_prob * state.pot) + ((1 - fold_prob) * (equity * final_pot - bet_size))
                
                result[(bet_action.name, bet_action.size)] = {"frequency": freq, 
                                    "ev": ev}
        return result
    
    # hero_prob responding to a bet by the villain after a check.
    def facing_check(self, state: GameState, legal_actions: list[Action], equity: float, hero_probs: dict[str, float] | None = None) -> dict[(str, float), dict]:
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
                return {(check_action.name, check_action.size): {"frequency": 1.0, "ev": equity * state.pot}}
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
            result[(check_action.name, check_action.size)] = {"frequency": check_freq,
                                    "ev": equity * state.pot}
        
        if bet_actions:
            freq = bet_freq / len(bet_actions)
            for bet_action in bet_actions:
                bet_size = bet_action.size - state.villain_amt

                if hero_probs and "FOLD" in hero_probs:
                    fold_prob = hero_probs["FOLD"]
                else:
                    # FIXED: Add the same scaling logic as facing_bet
                    bet_in_pot_units = bet_size / state.pot if state.pot > 0 else 1.0
                    
                    if bet_action.name == "ALL IN":
                        if bet_in_pot_units < 1.0:
                            fold_prob = 0.35 + 0.30 * bet_in_pot_units
                        elif bet_in_pot_units < 3.0:
                            fold_prob = 0.65 + 0.10 * (bet_in_pot_units - 1.0)
                        else:
                            fold_prob = min(0.85, 0.75 + 0.03 * (bet_in_pot_units - 3.0))
                    else:
                        fold_prob = min(0.50, 0.15 + 0.20 * bet_in_pot_units)
                
                final_pot = state.pot + 2 * bet_size
                ev = (fold_prob * state.pot) + ((1 - fold_prob) * (equity * final_pot - bet_size))
                
                result[(bet_action.name, bet_action.size)] = {"frequency": freq, 
                                    "ev": ev}
        return result