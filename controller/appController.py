from main.model.Deck import Deck
from .gameState import GameState, STREETS
from .action import Action
from main.model.Evaluator import Evaluator


class AppController:
    def __init__(self, state: GameState) -> None:
        self.state = state
        self.deck = Deck()
        self.deck.shuffle()
        self.state_change = None
        self.new_hand()
    
    def handle_action(self, action: Action) -> None:
        self.debug_state("HERO_ACTION_START")

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
        self.debug_state("HERO_ACTION_APPLIED")



        if self.state.hand_over:
            self.state.button_index = (self.state.button_index + 1) % 2
            self.new_hand()
            return

        if self.round_complete():
            self.advance_street()
            if self.state_change:
                self.state_change(self.state)
            return
        
        self.state.to_act_index = 1
        self.villain_act()

        if self.round_complete():
            self.advance_street()

        if self.state_change:
            self.state_change(self.state)

    def villain_act(self) -> None:
        self.debug_state("VILLAIN_ACTION_START")

        if self.state.hand_over or self.state.street == "SHOWDOWN" or self.state.to_act_index != 1:
            return

        if self.state.hand_over or self.state.to_act_index != 1:
            return
        
        if self.state.current_bet > self.state.villain_amt:
            action = Action("CALL", "villain")
        else:
            action = Action("CHECK", "villain")
        
        self.apply_action(action, hero=False)
        self.state.actions.append(action)
        self.state.actions_list.append(action)
        
        self.state.to_act_index = 0

        if self.state_change:
            self.state_change(self.state)


    def advance_street(self) -> None:
        if self.state.street == "RIVER":
            self.state.street = "SHOWDOWN"
            self.evaluate_showdown()
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

        
    def round_complete(self) -> bool:
        print(f"[ROUND_COMPLETE_CHECK] street={self.state.street}, actions={len(self.state.actions)}, hero_amt={self.state.hero_amt}, villain_amt={self.state.villain_amt}, current_bet={self.state.current_bet}")

        if self.state.hand_over:
            print("[ROUND_COMPLETE] TRUE")
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
        
        print("[ROUND_COMPLETE] FALSE")

        return False
    
    def apply_action(self, action: Action, hero: bool = True) -> None:
        if action.name == "FOLD":
            self.state.hand_over = True
            self.state.street = "SHOWDOWN"
            return
        
        if action.name == "CHECK":
            pass

        elif action.name == "CALL":
            self.apply_call(hero)

        elif action.name == "RAISE" and action.size is not None:
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
    
    def apply_raise(self, size: float, hero: bool = True) -> None:
        if self.state.current_bet == 0:
            new_bet = size
        else:
            new_bet = self.state.current_bet * size

        if hero:
            raise_amt = new_bet - self.state.hero_amt
            if raise_amt <= 0:
                return

            self.state.current_bet = new_bet
            self.state.hero_amt += raise_amt
            self.state.pot += raise_amt
            self.state.hero_stack -= raise_amt
        else:
            raise_amt = new_bet - self.state.villain_amt
            if raise_amt <= 0:
                return

            self.state.current_bet = new_bet
            self.state.villain_amt += raise_amt
            self.state.pot += raise_amt
            self.state.villain_stack -= raise_amt
    
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

    def post_big_blind(self):
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
            self.villain_act()
        else:
            self.state.villain_stack -= bb
            self.state.villain_amt = bb
            self.state.to_act_index = 0
            self.state.pot = bb
            self.state.current_bet = bb
        

    def evaluate_showdown(self) -> None:
        print(">>> SHOWDOWN TRIGGERED <<<")

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

    def debug_state(self, tag=""):
        print(
            f"[{tag}] "
            f"street={self.state.street} | "
            f"actions={len(self.state.actions)} | "
            f"hero_amt={self.state.hero_amt} | "
            f"villain_amt={self.state.villain_amt} | "
            f"current_bet={self.state.current_bet} | "
            f"to_act={self.state.to_act_index}"
        )

    
