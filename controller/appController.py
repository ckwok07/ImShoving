from main.model.Deck import Deck
from .gameState import GameState, STREETS
from .action import Action
from main.model.Evaluator import Evaluator
from main.model.Simulator import Simulator
import random


class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
        self.deck = Deck()
        self.deck.shuffle()
        self.state_change = None
        self.new_hand()
        self.cached_hero_equity = None
    
    def handle_action(self, action: Action) -> None:

        if self.state.hand_over:
            return
        elif self.state.to_act_index != 0:
            return
        elif action.name == "CHECK" and self.state.current_bet > self.state.hero_amt:
            return
        elif action.name == "CALL" and self.state.current_bet == self.state.hero_amt:
            action = Action("CHECK", "hero")
        
        self.apply_action(action)
        self.state.actions.append(action)
        self.state.actions_list.append(action)



        if self.state.hand_over:
            self.state.button_index = (self.state.button_index + 1) % 2
            self.new_hand()
            return

        if self.round_complete():
            if self.state.street == "RIVER":
                self.state.street = "SHOWDOWN"
                self.evaluate_showdown()
            else:
                self.advance_street()
            return

        
        self.state.to_act_index = 1
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
        
        
        if self.state.current_bet > self.state.villain_amt:
            action = Action("CALL", "villain")
        else:
            action = Action("CHECK", "villain")
        
        
        # if self.state.current_bet > self.state.villain_amt:
        #     choice = random.choice([1,2,3])
        #     if choice == 1:
        #         action = Action("CALL", "villain")
        #     elif choice == 2:
        #         action = Action("RAISE", "villain", 2 * self.state.current_bet)
        #     else:
        #         action = Action("FOLD", "villain")
        # else:
        #     if random.choice([True, False]):
        #         action = Action("CHECK", "villain")
        #     else:
        #         action = Action("BET", "villain", 2)
        
        self.apply_action(action, hero=False)
        self.state.actions_list.append(action)

        if self.state.hand_over:

            return

        self.state.actions.append(action)
        
        self.state.to_act_index = 0

        if self.state_change:
            self.state_change(self.state)

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
            self.state.board.extend(self.deck.deal(3))
        elif nxt == "TURN" or nxt == "RIVER":
            self.state.board.extend(self.deck.deal(1))

        self.state.current_bet = 0
        self.state.hero_amt = 0
        self.state.villain_amt = 0
        
        self.state.to_act_index = 1 - self.state.button_index

        if self.state_change:
            self.state_change(self.state)
        
        if self.state.hero_all_in and self.state.villain_all_in:
            self.advance_street()
        elif (self.state.hero_all_in or self.state.villain_all_in) and self.state.hero_amt == self.state.villain_amt:
            self.advance_street()
        else:
            if self.state.to_act_index == 1:
                self.villain_act()
        
        self.cached_hero_equity = None
    
    def round_complete(self) -> bool:

        if self.state.hand_over:
            return True
        
        if self.state.hero_all_in and self.state.villain_all_in:
            return True
        
        # Count actions this street (actions get cleared in advance_street)
        action_count = len(self.state.actions)
        
        # Need at least one action from each player
        if action_count < 2:
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
            else:
                self.state.hero_stack += self.state.pot

            self.state.pot = 0
            self.state.hand_over = True
            self.state.street = "SHOWDOWN"

            if self.state_change:
                self.state_change(self.state)

            return
        
        if action.name == "CHECK":
            pass

        elif action.name == "CALL":
            self.apply_call(hero)

        elif action.name == "RAISE" or action.name == "BET" and action.size is not None:
            self.apply_raise(action.size, hero)

        elif action.name == "ALL IN":
            self.apply_all_in(hero)

    def apply_call(self, hero: bool = True) -> None:
        if hero:
            amount = self.state.current_bet - self.state.hero_amt
            if amount <= 0:
                return
            
            amount = min(amount, self.state.hero_stack)
            self.state.hero_amt += amount
            self.state.pot += amount
            self.state.hero_stack -= amount

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
    
    def apply_all_in(self, hero: bool = True) -> None:
        if hero:
            all_in_amt = self.state.hero_stack
            self.state.hero_stack = 0
            self.state.hero_amt += all_in_amt
            self.state.pot += all_in_amt
            
            if self.state.hero_amt > self.state.current_bet:
                self.state.current_bet = self.state.hero_amt
            
            self.state.hero_all_in = True
        else:
            all_in_amt = self.state.villain_stack
            self.state.villain_stack = 0
            self.state.villain_amt += all_in_amt
            self.state.pot += all_in_amt
            
            if self.state.villain_amt > self.state.current_bet:
                self.state.current_bet = self.state.villain_amt
            
            self.state.villain_all_in = True

    def new_hand(self) -> None:
        self.state.to_act_index = self.state.button_index

        self.state.hand_over = False
        self.deck = Deck()
        self.deck.shuffle()
        self.cached_hero_equity = None

        self.state.street = "PREFLOP"
        self.state.board.clear()

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

    def post_big_blind(self) -> None:
        bb = 1
        bb_player = 1 - self.state.button_index

        self.state.hero_amt = 0
        self.state.villain_amt = 0

        if bb_player == 0:
            self.state.hero_stack -= bb
            self.state.hero_amt = bb
            self.state.to_act_index = 1
            self.state.pot = bb
            self.state.current_bet = bb
            self.state.actions_list.append(Action(name = "Post Blind", player = "hero", size = bb))
            self.villain_act()
        else:
            self.state.villain_stack -= bb
            self.state.villain_amt = bb
            self.state.to_act_index = 0
            self.state.pot = bb
            self.state.current_bet = bb
            self.state.actions_list.append(Action(name = "Post Blind", player = "villain", size = bb))
        
    def evaluate_showdown(self) -> None:
        hero_cards = self.state.hero_hand + self.state.board
        villain_cards = self.state.villain_hand + self.state.board

        hero_best = Evaluator.best_hand(hero_cards)
        villain_best = Evaluator.best_hand(villain_cards)
        result = Evaluator.compare_hands(hero_best, villain_best)

        if result == 1:  # hero wins
            self.state.hero_stack += self.state.pot
        elif result == -1:  # villain wins
            self.state.villain_stack += self.state.pot
        else:  # tie
            half_pot = self.state.pot / 2
            self.state.hero_stack += half_pot
            self.state.villain_stack += half_pot
        
        self.state.hand_over = True
        
        if self.state_change:
            self.state_change(self.state)
    
    def get_hero_legal_actions(self) -> list[Action]:
        actions = []

        if self.state.hand_over or self.state.to_act_index != 0:
            return actions
        
        bet_exists = self.state.current_bet > 0
        facing_bet = self.state.current_bet > self.state.hero_amt


        if facing_bet:
            actions.append(Action("FOLD", "hero"))
            actions.append(Action("CALL", "hero"))

            for new_bet in (self.state.current_bet * 2, self.state.current_bet * 4):
                raise_cost = new_bet - self.state.hero_amt
                if raise_cost > 0 and self.state.hero_stack >= raise_cost:
                    actions.append(Action("RAISE", "hero", size = new_bet))
        elif bet_exists:
            actions.append(Action("FOLD", "hero"))
            actions.append(Action("CHECK", "hero"))

            for new_bet in (self.state.current_bet * 2, self.state.current_bet * 4):
                cost = new_bet - self.state.hero_amt
                if cost > 0 and self.state.hero_stack >= cost:
                    actions.append(Action("RAISE", "hero", size=new_bet))
        else:
            actions.append(Action("FOLD", "hero"))
            actions.append(Action("CHECK", "hero"))

            for bet in (1, 2, 4):
                if self.state.hero_stack >= bet:
                    actions.append(Action("BET", "hero", size = bet))
        
        if self.state.hero_stack > 0 and not self.state.hero_all_in:
            actions.append(Action("ALL IN", "hero"))

        self.compute_hero_equity()
        self.compute_action_EVs(actions)

        for action in actions:
            print(f"{action.name}, {action.size}, {action.ev: .2f}")
        
        return actions
    
    def compute_hero_equity(self) -> float:
        if self.cached_hero_equity is None:
            numTrials = 5000 if self.state.street == "PREFLOP" else 12000
            self.cached_hero_equity = Simulator.simulate_equity(hand = self.state.hero_hand, 
                                                            board = self.state.board,
                                                            players = 2,
                                                            trials = numTrials)
        
        return self.cached_hero_equity
    
    def compute_action_EVs(self, actions: list[Action]) -> list[Action]:
        for action in actions:
            if action.name == "FOLD":
                action.ev = 0
            elif action.name == "CHECK":
                ev_villain_checks = 0.5 * (self.cached_hero_equity * self.state.pot)
                final_pot_if_bet = self.state.pot + 2 + 2
                ev_villain_bets = 0.5 * (self.cached_hero_equity * final_pot_if_bet - 2)
            
                action.ev = ev_villain_checks + ev_villain_bets

            elif action.name == "CALL":
                cost = max(self.state.current_bet - self.state.hero_amt, 0)
                final_pot = self.state.pot + cost
                action.ev = self.cached_hero_equity * final_pot - cost

            elif action.name == "BET":
                fold_prob = 1/3
                call_prob = 1/3
                raise_prob = 1/3

                cost = max(action.size, 0)
                ev_fold = fold_prob * self.state.pot
                ev_call = call_prob * (self.cached_hero_equity * (self.state.pot + 2 * cost) - cost)

                if 2 * cost - cost <= self.state.hero_stack:
                    ev_raise = raise_prob * max(self.cached_hero_equity * (self.state.pot + cost + 2 * cost + (2 * cost - cost)) - (cost + (2 * cost - cost)), 0)
                else:
                    ev_raise = 0
    
                action.ev = ev_fold + ev_call + ev_raise
            elif action.name == "RAISE":
                fold_prob = 1/3
                call_prob = 1/3
                raise_prob = 1/3

                cost = max(action.size - self.state.hero_amt, 0)
                
                ev_fold = fold_prob * self.state.pot
                
                ev_call = call_prob * (self.cached_hero_equity * (self.state.pot + 2 * cost) - cost)
                
                if 2 * action.size - action.size <= self.state.hero_stack - cost:
                    ev_raise = raise_prob * max(self.cached_hero_equity * (self.state.pot + cost + 2 * action.size + (2 * action.size - action.size)) - (cost + (2 * action.size - action.size)), 0)
                else:
                    ev_raise = 0
                
                action.ev = ev_fold + ev_call + ev_raise
            elif action.name == "ALL IN":
                cost = max(self.state.hero_stack, 0)
                fold_prob = 1/3
                call_prob = 2/3

                ev_fold = fold_prob * self.state.pot
                final_pot = self.state.pot + cost + min(cost, self.state.villain_stack)
                ev_call = call_prob * (self.cached_hero_equity * final_pot - cost)
                
                action.ev = ev_fold + ev_call

        return actions

    
