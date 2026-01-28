from main.model.Card import Card
from main.model.Deck import Deck
from main.model.Simulator import Simulator

import json
import os
import time

def generateHands() -> list[list[Card]]:
    deck = Deck()
    cards = deck.cards
    hands = []

    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            hands.append([cards[i], cards[j]])

    return hands

def hand_to_key(hand: list[Card]) -> str:
    c1, c2 = hand

    if (c2.rank, c2.suit) > (c1.rank, c1.suit):
        c1, c2 = c2, c1

    return c1.display() + c2.display()


def main():
    all_hands = generateHands()
    print(f"number of hands: {len(all_hands)}")
    

    results = {}
    output_path = os.path.join("scripts", "data", "hand_equities.json")

    for idx, hand in enumerate(all_hands):
        c1 = hand[0]
        c2 = hand[1]
        
        key = hand_to_key(hand)

        hand_start = time.perf_counter()

        equity = Simulator.simulate_equity(hand=hand, players=2, trials=100000)

        hand_end = time.perf_counter()
        hand_time = hand_end - hand_start

        print(f"[{idx+1}/{len(all_hands)}] {key} equity={equity:.4f}  time={hand_time:.2f}s")


        results[key] = {
            "card1Rank": c1.rank,
            "card1Suit": c1.suit,
            "card2Rank": c2.rank,
            "card2Suit": c2.suit,
            "equity": equity
        }


        if idx % 25 == 0 and idx > 0:
            with open(output_path, "w") as f:
                json.dump(results, f)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()