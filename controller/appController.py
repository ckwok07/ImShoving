from math import sqrt
from controller.decisionAccuracy import DecisionQuality, ACCURACY_LABELS
from main.model.Deck import Deck
from .gameState import GameState, STREETS
from .action import Action
from main.model.Evaluator import Evaluator
from main.model.Simulator import Simulator
import random
import threading
from typing import Optional, Callable
from PyQt6.QtCore import Qt, QTimer
from controller.villain.Villain import Villain


class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
        self.deck = Deck()
        self.deck.shuffle()
        self.state_change = None
        self.villain = Villain()
        self.new_hand()
        self.cached_hero_equity = None
        self.decision_quality = []
        self.last_hero_actions = []
        self._equity_thread: Optional[threading.Thread] = None
        self.show_villain_cards = False
    
    def handle_action(self, action: Action) -> None:
        if self.state.animating:
            return
        elif self.state.hand_over:
            return
        elif self.state.to_act_index != 0:
            return
        elif action.name == "CHECK" and self.state.current_bet > self.state.hero_amt:
            return
        elif action.name == "CALL" and self.state.current_bet == self.state.hero_amt:
            action = Action("CHECK", "hero")
        
        if action.player == "hero":
            self.analyze_decision(action)

        self.apply_action(action)
        action.pot_after = self.state.pot
        self.state.actions.append(action)
        self.state.actions_list.append(action)

        if self.round_complete():
            if self.state.street == "RIVER":
                self.state.street = "SHOWDOWN"
                self.evaluate_showdown()
            else:
                self.advance_street()
            return

        
        self.state.to_act_index = 1
        if not self.round_complete() and not self.state.hand_over:
            self.villain_act()


        if self.round_complete():
            self.advance_street()

        if self.state_change:
            self.state_change(self.state)
        
        self.cached_hero_equity = None

    def villain_act(self) -> None:

        if self.state.hand_over or self.state.street == "SHOWDOWN" or self.state.to_act_index != 1:
            return

        if self.state.hand_over or self.state.to_act_index != 1:
            return
        
        self.state.animating = True
        # if self.state.current_bet > self.state.villain_amt:
        #     action = Action("CALL", "villain")
        # else:
        #     action = Action("CHECK", "villain")
        # def do_villain_action():
        #     self.state.animating = False
        #     self.villain.choose_action(self.state)
        #     if self.state.villain_all_in:
        #         if self.round_complete():
        #             if self.state.street == "RIVER":
        #                 self.state.street = "SHOWDOWN"
        #                 self.evaluate_showdown()
        #             else:
        #                 self.advance_street()
        #         else:
        #             self.state.to_act_index = 0
        #         self.state.animating = False
        #         if self.state_change:
        #             self.state_change(self.state)
        #         return

        #     elif self.state.current_bet > self.state.villain_amt:
        #         if self.state.hero_all_in:
        #             if random.choice([True, False]):
        #                 action = Action("CALL", "villain", min(self.state.current_bet - self.state.villain_amt, self.state.villain_stack))
        #             else:
        #                 action = Action("FOLD", "villain", 0)
        #         else:
        #             choice = random.choice([1,2,3])
        #             if choice == 1:
        #                 action = Action("CALL", "villain", min(self.state.current_bet - self.state.villain_amt, self.state.villain_stack))
        #             elif choice == 2:
        #                 action = Action("RAISE", "villain", min(2 * self.state.current_bet, self.state.villain_amt + self.state.villain_stack))
        #             else:
        #                 action = Action("FOLD", "villain", 0)
        #     else:
        #         if random.choice([True, False]):
        #             action = Action("CHECK", "villain", 0)
        #         else:
        #             action = Action("BET", "villain", min(2, self.state.villain_stack))

        #     if self.state.villain_stack <= 0:
        #         self.state.villain_all_in = True

        #     self.state.actions_list.append(action)
        #     self.apply_action(action, hero=False)
        #     action.pot_after = self.state.pot

        #     if self.state.hand_over:
        #         self.state.animating = False
        #         if self.state_change:
        #             self.state_change(self.state)
        #         return

        #     self.state.actions.append(action)
            
        #     if self.round_complete() or self.state.hero_all_in:
        #         if self.state.street == "RIVER":
        #             self.state.street = "SHOWDOWN"
        #             self.evaluate_showdown()
        #         else:
        #             self.advance_street()
        #     else:
        #         self.state.to_act_index = 0

        #     self.state.animating = False

        #     if self.state_change:
        #         self.state_change(self.state)

        def do_villain_action():
            self.state.animating = False
            action = self.villain.choose_action(self.state)
            if self.state.villain_all_in:
                if self.round_complete():
                    if self.state.street == "RIVER":
                        self.state.street = "SHOWDOWN"
                        self.evaluate_showdown()
                    else:
                        self.advance_street()
                else:
                    self.state.to_act_index = 0
                self.state.animating = False
                if self.state_change:
                    self.state_change(self.state)
                return

            if self.state.villain_stack <= 0:
                self.state.villain_all_in = True

            self.state.actions_list.append(action)
            self.apply_action(action, hero=False)
            action.pot_after = self.state.pot

            if self.state.hand_over:
                self.state.animating = False
                if self.state_change:
                    self.state_change(self.state)
                return

            self.state.actions.append(action)
            
            if self.round_complete() or self.state.hero_all_in:
                if self.state.street == "RIVER":
                    self.state.street = "SHOWDOWN"
                    self.evaluate_showdown()
                else:
                    self.advance_street()
            else:
                self.state.to_act_index = 0

            self.state.animating = False

            if self.state_change:
                self.state_change(self.state)

        QTimer.singleShot(2000, do_villain_action)

    def advance_street(self) -> None:
        if self.state.street == "RIVER":
            self.state.street = "SHOWDOWN"
            self.evaluate_showdown()
            return
        elif self.state.street == "SHOWDOWN":
            return

        index = STREETS.index(self.state.street)
        nxt = STREETS[index + 1]
        self.state.street = nxt
        self.state.actions.clear()

        if nxt == "FLOP":
            flop = self.deck.deal(3)
            self.state.actions_list.append(Action(name = "FLOP", player = "hero", size = 0, cards = flop))
            self.state.board.extend(flop)
        elif nxt == "TURN":
            turn = (self.deck.deal(1))
            self.state.actions_list.append(Action(name = "TURN", player = "hero", size = 0, cards = turn))
            self.state.board.extend(turn)
        elif nxt == "RIVER":
            river = (self.deck.deal(1))
            self.state.actions_list.append(Action(name = "RIVER", player = "hero", size = 0, cards = river))
            self.state.board.extend(river)

        self.state.current_bet = 0
        self.state.hero_amt = 0
        self.state.villain_amt = 0
        
        self.state.to_act_index = 1 - self.state.button_index

        if self.state_change:
            self.state_change(self.state)
        
        if nxt == "FLOP":
            animation_time = 3 * 500 + 400
        else:
            animation_time = 1 * 500 + 400
        
        if self.state.hero_all_in and self.state.villain_all_in:
            QTimer.singleShot(animation_time, lambda: self.advance_street())
        elif (self.state.hero_all_in or self.state.villain_all_in) and self.state.hero_amt == self.state.villain_amt:
            QTimer.singleShot(animation_time, lambda: self.advance_street())
        else:
            if self.state.to_act_index == 1:
                QTimer.singleShot(animation_time, self.villain_act)
        
        self.cached_hero_equity = None
        self.compute_hero_equity()
    
    def round_complete(self) -> bool:

        if self.state.hand_over:
            return True
        
        if self.state.hero_all_in and self.state.villain_all_in:
            return True
        
        action_count = len(self.state.actions)
        
        if action_count < 2 and not (self.state.hero_all_in or self.state.villain_all_in):
            return False

        if (self.state.hero_amt == self.state.villain_amt and 
            self.state.hero_amt == self.state.current_bet):
            return True


        return False
    
    def apply_action(self, action: Action, hero: bool = True) -> None:
        if action.name == "FOLD":
            # award pot
            if hero:
                self.state.villain_stack += self.state.pot
                self.state.hero_action_count += 1
                self.state.hero_fold_count += 1
            else:
                self.state.hero_stack += self.state.pot
                self.state.villain_action_count += 1
                self.state.villain_fold_count += 1

            self.state.pot = 0
            self.state.hand_over = True
            if self.state.actions_list: 
                self.villain.observe_hero(self.state)
            self.state.street = "SHOWDOWN"

            if self.state_change:
                self.state_change(self.state)

            return
        
        if action.name == "CHECK":
            if hero:
                self.state.hero_action_count += 1
                self.state.hero_check_count += 1
            else:
                self.state.villain_action_count += 1
                self.state.villain_check_count += 1
            pass

        elif action.name == "CALL":
            self.apply_call(hero)

        elif action.name in ("RAISE", "BET"):
            if hero:
                if action.name == "BET":
                    self.state.hero_action_count += 1
                    self.state.hero_bet_count += 1
                else:
                    self.state.hero_action_count += 1
                    self.state.hero_raise_count += 1
            else:
                if action.name == "BET":
                    self.state.villain_action_count += 1
                    self.state.villain_bet_count += 1
                else:
                    self.state.villain_action_count += 1
                    self.state.villain_raise_count += 1
            self.apply_raise(action.size, hero)

        elif action.name == "ALL IN":
            self.apply_all_in(action.size, hero)

    def apply_call(self, hero: bool = True) -> None:
        if hero and self.state.hero_stack == 0:
            return
        if hero:
            amount = self.state.current_bet - self.state.hero_amt
            if amount <= 0:
                return
            
            amount = min(amount, self.state.hero_stack)
            self.state.hero_amt += amount
            self.state.pot += amount
            self.state.hero_stack -= amount
            self.state.hero_action_count += 1
            self.state.hero_call_count += 1

            if self.state.hero_stack == 0:
                self.state.hero_all_in = True

        else:
            amount = self.state.current_bet - self.state.villain_amt
            if amount <= 0:
                return
            
            amount = min(amount, self.state.villain_stack)
            self.state.villain_amt += amount
            self.state.pot += amount
            self.state.villain_stack -= amount
            self.state.villain_action_count += 1
            self.state.villain_call_count += 1

            if self.state.villain_stack == 0:
                self.state.villain_all_in = True
    
    def apply_raise(self, new_bet: float, hero: bool = True) -> None:
        if hero:
            raise_amt = new_bet - self.state.hero_amt
            if raise_amt <= 0:
                return
            
            raise_amt = min(raise_amt, self.state.hero_stack)

            self.state.current_bet = new_bet
            self.state.hero_amt += raise_amt
            self.state.pot += raise_amt
            self.state.hero_stack -= raise_amt

            if self.state.hero_stack == 0:
                self.state.hero_all_in = True

        else:
            raise_amt = new_bet - self.state.villain_amt
            if raise_amt <= 0:
                return
            
            raise_amt = min(raise_amt, self.state.villain_stack)

            self.state.current_bet = new_bet
            self.state.villain_amt += raise_amt
            self.state.pot += raise_amt
            self.state.villain_stack -= raise_amt

            if self.state.villain_stack == 0:
                self.state.villain_all_in = True
    
    def apply_all_in(self, size: int, hero: bool = True) -> None:
        if hero:
            all_in_amt = size
            old_current_bet = self.state.current_bet
            
            self.state.hero_stack -= all_in_amt 
            self.state.hero_amt += all_in_amt
            self.state.pot += all_in_amt
            
            self.state.hero_action_count += 1
            
            if self.state.hero_amt > old_current_bet:
                self.state.current_bet = self.state.hero_amt
                if old_current_bet == 0:
                    self.state.hero_bet_count += 1
                else:
                    self.state.hero_raise_count += 1
            else:
                self.state.hero_call_count += 1
            
            self.state.hero_all_in = True
            
        else:
            all_in_amt = self.state.villain_stack
            old_current_bet = self.state.current_bet
            
            self.state.villain_stack -= all_in_amt
            self.state.villain_amt += all_in_amt
            self.state.pot += all_in_amt
            
            self.state.villain_action_count += 1
            
            if self.state.villain_amt > old_current_bet:
                self.state.current_bet = self.state.villain_amt
                if old_current_bet == 0:
                    self.state.villain_bet_count += 1
                else:
                    self.state.villain_raise_count += 1
            else:
                self.state.villain_call_count += 1
            
            self.state.villain_all_in = True

    def new_hand(self) -> None:
        print(f"START OF new_hand(): button_index = {self.state.button_index}")
        print("GameState id:", id(self.state))
        assert self.state.hero_action_count == (
        self.state.hero_check_count + 
        self.state.hero_fold_count + 
        self.state.hero_call_count + 
        self.state.hero_raise_count + 
        self.state.hero_bet_count)

        assert self.state.villain_action_count == (
        self.state.villain_check_count + 
        self.state.villain_fold_count + 
        self.state.villain_call_count + 
        self.state.villain_raise_count + 
        self.state.villain_bet_count)

        print(f"BEFORE: button_index = {self.state.button_index}")
        self.state.button_index = (self.state.button_index + 1) % 2
        print(f"AFTER: button_index = {self.state.button_index}")
        
        # self.state.to_act_index = self.state.button_index
        self.state.show_villain_cards = False

        self.state.hand_over = False
        self.cached_hero_equity = None

        self.state.hero_hand = None
        self.state.villain_hand = None
        self.state.board.clear()

        if self.state_change:
            self.state_change(self.state)

        self.deck = Deck()
        self.deck.shuffle()
        

        self.state.street = "PREFLOP"

        self.state.current_bet = 0
        self.state.hero_amt = 0
        self.state.villain_amt = 0
        self.state.pot = 0
        self.state.hero_all_in = False
        self.state.villain_all_in = False
        self.state.actions_list = []

        self.state.actions.clear()

        self.state.hero_hand = self.deck.deal(2)
        self.state.villain_hand = self.deck.deal(2)

        self.post_big_blind()

        if self.state_change:
            self.state_change(self.state)
        
        print(f"END OF new_hand(): button_index = {self.state.button_index}")

    def post_big_blind(self) -> None:
        bb = 1
        bb_player = 1 - self.state.button_index
        print(f"BB player: {bb_player}, Button: {self.state.button_index}")

        self.state.hero_amt = 0
        self.state.villain_amt = 0

        if bb_player == 0:
            self.state.hero_stack -= bb
            if self.state.hero_stack == 0:
                self.state.hero_all_in = True
            self.state.hero_amt = bb
            self.state.to_act_index = 1
            self.state.pot = bb
            self.state.current_bet = bb
            action = Action(name = "Post Blind", player = "hero", size = bb)
            action.pot_after = self.state.pot
            self.state.actions_list.append(action)
            self.villain_act()
        else:
            self.state.villain_stack -= bb
            if self.state.villain_stack == 0:
                self.state.villain_all_in = True
            self.state.villain_amt = bb
            self.state.to_act_index = 0
            self.state.pot = bb
            self.state.current_bet = bb
            if self.state.villain_stack == 0:
                self.state.villain_all_in = True

            action = Action(name = "Post Blind", player = "villain", size = bb)
            action.pot_after = self.state.pot
            self.state.actions_list.append(action)
        
        
    def evaluate_showdown(self) -> None:
        self.state.show_villain_cards = True

        hero_cards = self.state.hero_hand + self.state.board
        villain_cards = self.state.villain_hand + self.state.board

        hero_best = Evaluator.best_hand(hero_cards)
        villain_best = Evaluator.best_hand(villain_cards)
        result = Evaluator.compare_hands(hero_best, villain_best)

        if result == 1:  # hero wins
            self.state.hero_stack += self.state.pot
            self.state.actions_list.append(Action("SHOWDOWN", "hero", size = 0, cards = hero_best, cards2 = villain_best))
        elif result == -1:  # villain wins
            self.state.villain_stack += self.state.pot
            self.state.actions_list.append(Action("SHOWDOWN", "villain", size = 0, cards = villain_best, cards2 = hero_best))
        else:  # tie
            half_pot = self.state.pot / 2
            self.state.hero_stack += half_pot
            self.state.villain_stack += half_pot
            self.state.actions_list.append(Action("SHOWDOWN", "tie", size = 0, cards = hero_best, cards2 = villain_best))
        
        self.state.hand_over = True
        if self.state.actions_list: 
            self.villain.observe_hero(self.state)
        
        if self.state_change:
            self.state_change(self.state)
    
    def get_hero_legal_actions(self) -> list[Action]:
        actions = []

        if self.state.animating:
            return actions
        
        if self.state.hero_hand is None:
            return actions

        if self.state.hero_all_in or self.state.hero_stack == 0:
            return actions

        if self.state.hand_over or self.state.to_act_index != 0:
            return actions
        
        facing_bet = self.state.current_bet > self.state.hero_amt
        is_preflop = self.state.street == "PREFLOP"
        hero_is_bb = self.state.hero_amt == self.state.current_bet and self.state.current_bet > 0
        bb_option = is_preflop and hero_is_bb and not facing_bet
        max_affordable = self.state.villain_stack + self.state.villain_amt


        if facing_bet:
            actions.append(Action("FOLD", "hero", 0))
            
            if self.state.villain_all_in:
                call_amount = min(self.state.current_bet - self.state.hero_amt, self.state.hero_stack)
                actions.append(Action("CALL", "hero", call_amount))
            else:
                actions.append(Action("CALL", "hero", self.state.current_bet - self.state.hero_amt))

                for new_bet in (self.state.current_bet * 2, self.state.current_bet * 4):
                    raise_cost = new_bet - self.state.hero_amt
                    if raise_cost > 0 and self.state.hero_stack >= raise_cost and new_bet <= max_affordable:
                        actions.append(Action("RAISE", "hero", size = new_bet))
                
                if self.state.hero_stack > 0 and not self.state.hero_all_in:
                    max_effective_all_in = min(self.state.hero_stack, 
                                                self.state.villain_stack + self.state.villain_amt - self.state.hero_amt)
                    if max_effective_all_in > 0:
                        actions.append(Action("ALL IN", "hero", max_effective_all_in))

        elif bb_option:
            actions.append(Action("CHECK", "hero", 0))

            for new_bet in (self.state.current_bet * 2, self.state.current_bet * 4):
                cost = new_bet - self.state.hero_amt
                if cost > 0 and self.state.hero_stack >= cost and new_bet <= max_affordable:
                    actions.append(Action("RAISE", "hero", size=new_bet))
            
            if self.state.hero_stack > 0 and not self.state.hero_all_in:
                max_effective_all_in = min(self.state.hero_stack, 
                                            self.state.villain_stack + self.state.villain_amt - self.state.hero_amt)
                actions.append(Action("ALL IN", "hero", max_effective_all_in))

        else:
            actions.append(Action("CHECK", "hero", 0))

            for bet in (1, 2, 4):
                if self.state.hero_stack >= bet:
                    actions.append(Action("BET", "hero", size = bet))

            if self.state.hero_stack > 0 and not self.state.hero_all_in:
                max_effective_all_in = min(self.state.hero_stack, 
                                            self.state.villain_stack + self.state.villain_amt - self.state.hero_amt)
                actions.append(Action("ALL IN", "hero", max_effective_all_in))

        self.compute_hero_equity()
        if self._equity_thread and self._equity_thread.is_alive():
            self._equity_thread.join()

        self.compute_action_EVs(actions)

        # for action in actions:
        #     print(f"{action.name}, {action.size}, {action.ev: .2f}")
        
        self.last_hero_actions = actions
        return actions
    
    def compute_hero_equity(self) -> float:
        if self.state.hero_hand is None:
            return None
        
        if self.cached_hero_equity is None:
            if self._equity_thread is None or not self._equity_thread.is_alive():
                def calculate():
                    numTrials = 5000 if self.state.street == "PREFLOP" else 12000
                    self.cached_hero_equity = Simulator.simulate_equity(hand = self.state.hero_hand, 
                                                                    board = self.state.board,
                                                                    players = 2,
                                                                    trials = numTrials)
                self._equity_thread = threading.Thread(target = calculate, daemon = True)
                self._equity_thread.start()
        
        return self.cached_hero_equity
    
    def compute_action_EVs(self, actions: list[Action]) -> list[Action]:
        for action in actions:
            if self.cached_hero_equity is None:
                action.ev = 0
                continue
            if action.name == "FOLD":
                action.ev = 0
            elif action.name == "CHECK":
                villain_check_or_bet = self.state.villain_check_count + self.state.villain_bet_count
                if villain_check_or_bet > 50:
                    villain_checks_prob = self.state.villain_check_count / villain_check_or_bet
                    villain_bet_prob = self.state.villain_bet_count / villain_check_or_bet
                    ev_villain_checks = villain_checks_prob * (self.cached_hero_equity * self.state.pot)
                    final_pot_if_bet = self.state.pot + 2 + 2
                    ev_villain_bets = villain_bet_prob * (self.cached_hero_equity * final_pot_if_bet - 2)
                else:
                    ev_villain_checks = .5 * (self.cached_hero_equity * self.state.pot)
                    final_pot_if_bet = self.state.pot + 2 + 2
                    ev_villain_bets = .5 * (self.cached_hero_equity * final_pot_if_bet - 2)
            
                action.ev = ev_villain_checks + ev_villain_bets

            elif action.name == "CALL":
                cost = max(self.state.current_bet - self.state.hero_amt, 0)
                final_pot = self.state.pot + cost
                action.ev = self.cached_hero_equity * final_pot - cost

            elif action.name == "BET":
                villain_fold_call_raise = self.state.villain_fold_count + self.state.villain_call_count + self.state.villain_raise_count
                if villain_fold_call_raise > 50:
                    fold_prob = self.state.villain_fold_count / villain_fold_call_raise
                    call_prob = self.state.villain_call_count / villain_fold_call_raise
                    raise_prob = self.state.villain_raise_count / villain_fold_call_raise
                    cost = max(action.size, 0)

                    ev_fold = fold_prob * self.state.pot
                    ev_call = call_prob * (self.cached_hero_equity * (self.state.pot + 2 * cost) - cost)

                    if cost <= self.state.hero_stack:
                        ev_raise = raise_prob * max(self.cached_hero_equity * (self.state.pot + cost + 2 * cost + (2 * cost - cost)) - (cost + (2 * cost - cost)), 0)
                    else:
                        ev_raise = 0
                else:
                    fold_prob = 1/3
                    call_prob = 1/3
                    raise_prob = 1/3

                    cost = max(action.size, 0)
                    ev_fold = fold_prob * self.state.pot
                    ev_call = call_prob * (self.cached_hero_equity * (self.state.pot + 2 * cost) - cost)

                    if cost <= self.state.hero_stack:
                        ev_raise = raise_prob * max(self.cached_hero_equity * (self.state.pot + cost + 2 * cost + (2 * cost - cost)) - (cost + (2 * cost - cost)), 0)
                    else:
                        ev_raise = 0
    
                action.ev = ev_fold + ev_call + ev_raise
            elif action.name == "RAISE":
                villain_fold_call_raise = self.state.villain_fold_count + self.state.villain_call_count + self.state.villain_raise_count
                if villain_fold_call_raise > 50:
                    fold_prob = self.state.villain_fold_count / villain_fold_call_raise
                    call_prob = self.state.villain_call_count / villain_fold_call_raise
                    raise_prob = self.state.villain_raise_count / villain_fold_call_raise
                    cost = max(action.size - self.state.hero_amt, 0)

                    ev_fold = fold_prob * self.state.pot
                    ev_call = call_prob * (self.cached_hero_equity * (self.state.pot + 2 * cost) - cost)

                    if 2 * action.size - action.size <= self.state.hero_stack - cost:
                        ev_raise = raise_prob * max(self.cached_hero_equity * (self.state.pot + cost + 2 * action.size + (2 * action.size - action.size)) - (cost + (2 * action.size - action.size)), 0)
                    else:
                        ev_raise = 0
                else: 
                    cost = max(action.size - self.state.hero_amt, 0)
                    pot_before = self.state.pot
                    bet_to_pot_ratio = cost / max(pot_before, 0.1)
                    

                    base_fold = 0.55
                    base_call = 0.35
                    base_raise = 0.10
                    
                    size_factor = min(2.0, sqrt(bet_to_pot_ratio))
                    
                    adjusted_fold = base_fold * size_factor
                    adjusted_call = base_call + (base_fold - adjusted_fold) * 0.7
                    adjusted_raise = base_raise + (base_fold - adjusted_fold) * 0.3

                    total = adjusted_fold + adjusted_call + adjusted_raise
                    fold_prob = adjusted_fold / total
                    call_prob = adjusted_call / total
                    raise_prob = adjusted_raise / total
                    
                    ev_fold = fold_prob * self.state.pot
                    
                    ev_call = call_prob * (self.cached_hero_equity * (self.state.pot + 2 * cost) - cost)

                    villain_reraise_size = 2 * action.size
                    reraise_cost = villain_reraise_size - action.size
                    
                    if self.cached_hero_equity > 0.45:
                        final_pot_after_reraise = self.state.pot + cost + villain_reraise_size + reraise_cost
                        ev_hero_calls_reraise = self.cached_hero_equity * final_pot_after_reraise - (cost + reraise_cost)
                        ev_raise = raise_prob * ev_hero_calls_reraise
                    else:
                        ev_raise = raise_prob * (-cost)
                
                action.ev = ev_fold + ev_call + ev_raise

            elif action.name == "ALL IN":
                cost = max(action.size, 0)
                pot_before = self.state.pot
                bet_to_pot_ratio = cost / max(pot_before, 0.1)
                
                villain_fold_call = self.state.villain_fold_count + self.state.villain_call_count
                
                if villain_fold_call > 50:
                    base_fold_prob = self.state.villain_fold_count / villain_fold_call
                    base_call_prob = self.state.villain_call_count / villain_fold_call
                    
                    size_factor = min(2.5, 1.0 + (bet_to_pot_ratio ** 0.5) * 0.3)
                    adjusted_fold = min(0.95, base_fold_prob * size_factor)
                    adjusted_call = 1.0 - adjusted_fold
                    
                    fold_prob = adjusted_fold
                    call_prob = adjusted_call
                else:
                    if bet_to_pot_ratio > 10:
                        fold_prob = 0.75
                    elif bet_to_pot_ratio > 3:
                        fold_prob = 0.65
                    elif bet_to_pot_ratio > 1.5:
                        fold_prob = 0.55
                    elif bet_to_pot_ratio > 0.75:
                        fold_prob = 0.50
                    else:
                        fold_prob = 0.40
                    
                    call_prob = 1.0 - fold_prob
                
                if bet_to_pot_ratio > 10:
                    equity_multiplier = 0.35
                elif bet_to_pot_ratio > 5:
                    equity_multiplier = 0.50
                elif bet_to_pot_ratio > 3:
                    equity_multiplier = 0.65
                elif bet_to_pot_ratio > 1.5:
                    equity_multiplier = 0.80
                else:
                    equity_multiplier = 0.90
                
                equity_when_called = self.cached_hero_equity * equity_multiplier
                
                ev_fold = fold_prob * pot_before
                villain_call_amount = min(cost, self.state.villain_stack)
                final_pot = pot_before + cost + villain_call_amount
                ev_call = call_prob * (equity_when_called * final_pot - cost)
                
                action.ev = ev_fold + ev_call

        return actions
    
    def analyze_decision(self, hero_action: Action) -> None:
        actions = self.last_hero_actions

        best_ev = max(action.ev for action in actions)
        best_action = max(actions, key=lambda a: a.ev)
        best_action_name = f"{best_action.name} {best_action.size:.1f}"

        chosen_action = next(a for a in self.last_hero_actions 
                      if a.name == hero_action.name and a.size == hero_action.size)
        chosen_ev = chosen_action.ev

        pot = max(self.state.pot, 1)

        normalized_ev_loss = (best_ev - chosen_ev) / pot

        accuracy = max(0, 100 - 50 * normalized_ev_loss)

        decision_label = self.label_accuracy(accuracy)

        # if hero_action.ev < 0 and best_ev > 0:
        #     decision_label = "Mistake"


        decisionQuality = DecisionQuality(action_index = len(self.decision_quality), 
                                          action_name = hero_action.name,
                                          action_amount = f"{hero_action.size:.1f}",
                                          ev_chosen = chosen_ev,
                                          ev_best = best_ev,
                                          best_action = best_action_name,
                                          equity_before = self.cached_hero_equity,
                                          accuracy = accuracy,
                                          label = decision_label,
                                          hand = self.state.hero_hand,
                                          board = self.state.board,
                                          street = self.state.street)
        
        self.decision_quality.append(decisionQuality)

        if hasattr(self, 'accuracy_panel') and self.accuracy_panel:
            self.accuracy_panel.on_decision_made()
        
        print(f"label = {decision_label}, accuracy = {accuracy}")
    
    def label_accuracy(self, accuracy: float) -> str:
        for threshold in sorted(ACCURACY_LABELS.keys(), reverse=True):
            if accuracy >= threshold:
                return ACCURACY_LABELS[threshold]
            
    def reset_stacks(self):
        if not self.state.hand_over:
            return
        self.state.villain_stack = 100
        self.state.hero_stack = 100
        self.new_hand()


    
