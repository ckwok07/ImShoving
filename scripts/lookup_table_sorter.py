from collections import defaultdict
import json
import os

def key_to_hand(hand: str) -> str:
    if hand[0] == hand[2]:
        return f"{hand[0]}{hand[2]}"
    elif hand[1] == hand[3]: #suited
        return f"{hand[0]}{hand[2]}s"
    else:
        return f"{hand[0]}{hand[2]}o"

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(directory, "data", "hand_equities.json")
    with open(path) as file:
        data = json.load(file)

    output_path = os.path.join("scripts", "data", "hand_equities_aggregated.json")

    result = defaultdict(lambda: {"equity": None, "equity_list": [], "hand_list": []})
    for key, values in data.items():
        hand = key_to_hand(key)
        result[hand]["equity_list"].append(values["equity"])
        result[hand]["hand_list"].append(key)

    result = dict(result)

    for hand in result:
        result[hand]["equity"] = sum(result[hand]["equity_list"]) / len(result[hand]["hand_list"])

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(len(result))

if __name__ == "__main__":
    main()