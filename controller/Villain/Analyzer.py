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
        
        pot = 0

        for action in state.actions_list:
            if action.name == "Post Blind":
                pot += action.size
                continue

            action_key = self.action_to_key(action, pot)

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
            
            if action.name in ["BET", "RAISE", "ALL IN", "CALL"]:
                pot += action.size
            
            print(self.decision_tree)


    def action_to_key(self, action: Action, pot: float):
        if action.name == "SHOWDOWN":
            return None
    
        if action.name in ["FLOP", "TURN", "RIVER"]:
            return action.name
        
        player = "HERO" if action.player == "hero" else "VILLAIN"

        if action.name in ["CHECK", "FOLD", "CALL"]:
            return f"{player}_{action.name}"
        elif action.name in ["BET", "RAISE", "ALL IN"]:
            if pot <= 0:
                return f"{player}_{action.name}_UNKNOWN"
            
            ratio = action.size / pot
            
            if ratio < 0.40:
                bucket = "TINY"
            elif ratio < 0.75:
                bucket = "SMALL"
            elif ratio < 1.20:
                bucket = "POT"
            elif ratio < 1.75:
                bucket = "OVERBET1"
            elif ratio < 2.50:
                bucket = "OVERBET2"
            else:
                bucket = "OVERBET3"
            
            return f"{player}_{action.name}_{bucket}"
        
        return None
    
    def get_probabilities(self, state: GameState, villain_action: Action) -> dict[str, float] | None:
        position = "BB" if state.button_index == 0 else "D"
        current = self.decision_tree[position]
        
        pot = 0

        for action in state.actions_list:
            if action.name == "Post Blind":
                pot += action.size
                continue

            action_key = self.action_to_key(action, pot)
            if action_key is None:
                continue

            if action_key not in current:
                return None
            current = current[action_key]
            
            if action.name in ["BET", "RAISE", "ALL IN", "CALL"]:
                pot += action.size
        
        villain_action_key = self.action_to_key(villain_action, pot)
        if villain_action_key is None or villain_action_key not in current:
            return None
        
        current = current[villain_action_key]

        if "counts" not in current:
            return None
        
        counts = current["counts"]

        hero_counts = {}
        for action_key, count in counts.items():
            if action_key.startswith("HERO_"):
                action_type = action_key.replace("HERO_", "").split("_")[0]
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