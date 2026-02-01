from controller.gameState import GameState
from controller.action import Action

class Analyzer:
    def __init__(self):
        self.decision_tree = {"BB": {}, "D": {}}

    def update_tree(self, state: GameState) -> None:
        if not state.hand_over:
            return
        
        position = "BB" if state.button_index == 0 else "D"

        current = self.decision_tree[position]

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

            print(self.decision_tree)


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
    
    def get_probabilities(self, state: GameState, villain_action: Action) -> list[float] | None:
        position = "BB" if state.button_index == 0 else "D"

        current = self.decision_tree[position]

        for action in state.actions_list:
            if action.name == "Post Blind":
                continue

            action_key = self.action_to_key(action)
            if action_key is None:
                continue

            if action_key not in current:
                return None
            current = current[action_key]
        
        villain_action_key = self.action_to_key(villain_action)
        if villain_action_key is None or villain_action_key not in current:
            return None
        
        current = current[villain_action_key]

        if "counts" not in current:
            return None
        
        counts = current["counts"]

        hero_counts = {}
        for action_key, count in counts.items():
            if action_key.startswith("HERO_"):
                action_type = action_key.replace("HERO_", "").split("_")[0]  # "HERO_FOLD" → "FOLD"
                if action_type not in hero_counts:
                    hero_counts[action_type] = 0
                hero_counts[action_type] += count
        
        if not hero_counts:
            return None
        
        total = sum(hero_counts.values())
        if total < 5: 
            return None
        
        probabilities = {
            action: count / total 
            for action, count in hero_counts.items()
        }
        
        return probabilities