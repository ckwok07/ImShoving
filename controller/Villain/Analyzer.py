from controller.gameState import GameState
from controller.action import Action

class Analyzer:
    def __init__(self):
        self.preflop_flop_tree = {"BB": {}, "D": {}}
        self.postflop_count = {}

    def update_tree(self, state: GameState) -> None:
        if not state.hand_over:
            return
        
        position = "BB" if state.button_index == 0 else "D"

        current = self.preflop_flop_tree[position]

        for action in state.actions_list:
            if action.name == "Post Blind":
                continue

            action_key = self.action_to_key(action)

            if action_key is None:
                continue

            if "counts" not in current:
                current["counts"] = {}
            
            if action_key not in current["counts"]:
                current["counts"][action_key] = 0
            current["counts"][action_key] += 1

            if action_key not in current:
                current[action_key] = {}
        
            current = current[action_key]


    def action_to_key(self, action: Action):
        if action.name == "SHOWDOWN":
            return None
    
        if action.name in ["FLOP", "TURN", "RIVER"]:
            return action.name
        
        player = "HERO" if action.player == "hero" else "VILLAIN"

        if action.name in ["CHECK", "FOLD", "CALL"]:
            return f"{player}_{action.name}"
        elif action.name in ["BET", "RAISE", "ALL IN"]:
            return f"{player}_{action.name}"
        
        return None
    
    def get_probabilities(self, state: GameState, villain_action_key: Action) -> list[float] | None:
        pass