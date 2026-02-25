from controller.gameState import GameState
from controller.action import Action
from main.model.Simulator import Simulator
from main.model.Card import Card
from .Analyzer import Analyzer
from .GTOModel import GTOModel
import json
from pathlib import Path
import random
import math

class DecisionChooser:
    def __init__(self, analyzer: Analyzer):
        self.gto_model = GTOModel()
        self.analyzer = analyzer
        self.current_equity = None
        self.preflop_table = self.load_preflop_equity_table()

    def get_villain_decision(self, state: GameState) -> Action:
        legal_actions = self.get_villain_legal_actions(state)
        equity = self.get_equity(state)

        hero_probs = None
        for action in legal_actions:
            if action.name in ["BET", "CHECK", "RAISE", "CALL", "FOLD"]:
                hero_probs = self.analyzer.get_probabilities(state, action)
                if hero_probs:
                    break

        gto_actions = self.get_gto_strategy(state, legal_actions, equity, hero_probs)

        #gto_actions: {('FOLD', 0): {'frequency': 0.05, 'ev': 0}, 
        # ('CALL', 2): {'frequency': 0.45, 'ev': 2.478366666666666}, 
        # ('RAISE', 8): {'frequency': 0.16666666666666666, 'ev': 4.076324999999999}, 
        # ('RAISE', 16): {'frequency': 0.16666666666666666, 'ev': 5.033058333333329}, 
        # ('ALL IN', 98): {'frequency': 0.16666666666666666, 'ev': 14.839574999999982}}

        print(f"gto_actions:{gto_actions}")
        choice = random.uniform(0,1)
        print(choice)
        cumulative = 0

        for (action_name, action_size), freq_ev in gto_actions.items():
            cumulative += freq_ev["frequency"]
            if choice <= cumulative:
                return Action(name = action_name, player = "villain", size = action_size, ev = freq_ev["ev"])
            
        return Action("FOLD", "villain", 0, state.pot)
    
    def get_villain_legal_actions(self, state: GameState) -> list[Action]:
        actions = []

        if state.animating:
            return actions
        
        if state.villain_hand is None:
            return actions

        if state.villain_all_in or state.villain_stack == 0:
            return actions

        if state.hand_over or state.to_act_index != 1:
            return actions
        
        facing_bet = state.current_bet > state.villain_amt
        is_preflop = state.street == "PREFLOP"
        villain_is_bb = state.villain_amt == state.current_bet and state.current_bet > 0
        bb_option = is_preflop and villain_is_bb and not facing_bet
        max_affordable = state.hero_stack + state.hero_amt

        if facing_bet:
            actions.append(Action("FOLD", "villain", 0))

            if state.hero_all_in:
                call_amount =  min(state.current_bet - state.villain_amt, state.villain_stack)
                actions.append(Action("CALL", "villain", call_amount))
            else:
                actions.append(Action("CALL", "hero", state.current_bet - state.villain_amt))
                for new_bet in (state.current_bet * 2, state.current_bet * 4):
                    raise_cost = new_bet - state.villain_amt
                    if raise_cost > 0 and state.villain_stack >= raise_cost and new_bet <= max_affordable:
                        actions.append(Action("RAISE", "villain", size = new_bet))

                if state.villain_stack > 0 and not state.villain_all_in:
                    max_effective_all_in = min(state.villain_stack, state.hero_stack + state.hero_amt - state.villain_amt)
                    if max_effective_all_in > 0:
                        actions.append(Action("ALL IN", "villain", max_effective_all_in))
        elif bb_option:
            actions.append(Action("CHECK", "villain", 0))

            for new_bet in (state.current_bet * 2, state.current_bet * 4):
                cost = new_bet - state.villain_amt
                if cost > 0 and state.villain_stack >= cost and new_bet <= max_affordable:
                    actions.append(Action("RAISE", "villain", size=new_bet))
            if state.villain_stack > 0 and not state.villain_all_in:
                max_effective_all_in = min(state.villain_stack, state.hero_stack + state.hero_amt - state.villain_amt)
                if max_effective_all_in > 0:
                    actions.append(Action("ALL IN", "villain", max_effective_all_in))
        else:
            actions.append(Action("CHECK", "villain", 0))

            for bet in (1, 2, 4):
                if state.villain_stack >= bet:
                    actions.append(Action("BET", "villain", size = bet))
            
            if state.villain_stack > 0 and not state.villain_all_in:
                max_effective_all_in = min(state.villain_stack, state.hero_stack)
                if max_effective_all_in > 0:
                    actions.append(Action("ALL IN", "villain", max_effective_all_in))

        # if state.villain_stack > 0 and not state.villain_all_in:
        #     max_effective_all_in = min(state.villain_stack, 
        #                                 state.hero_stack + state.hero_amt - state.villain_amt)
        #     actions.append(Action("ALL IN", "villain", max_effective_all_in))

        print(f"legal actions: {actions}")
        return actions
    
    def get_gto_strategy(self, state: GameState, legal_actions: list[Action], equity: float, hero_probs: dict[str, float]) -> dict[str, float]:
        # facing bet or raise
        if state.current_bet > state.villain_amt: # facing bet
            return self.gto_model.facing_bet(state, legal_actions, equity, hero_probs)
            
        if state.street == "PREFLOP":
            villain_acts_first = bool(state.button_index == 1)
        else:
            villain_acts_first = bool(state.button_index == 0)

        # first to act
        if state.current_bet == 0 and state.villain_amt == 0 and villain_acts_first:
            return self.gto_model.first_to_act(state, legal_actions, equity, hero_probs)
        # facing a check
        else:
            return self.gto_model.facing_check(state, legal_actions, equity, hero_probs)

    def get_equity(self, state: GameState) -> float:
        if state.street == "PREFLOP":
            key = self.hand_to_key(state.villain_hand)
            return self.preflop_table[key]["avg_equity"]

        else:
            equity = Simulator.simulate_equity(hand = state.villain_hand,
                                             board = state.board,
                                             players = 2,
                                             trials = 15000)
            print(f"equity : {equity} for {state.villain_hand}")
            return equity
    
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