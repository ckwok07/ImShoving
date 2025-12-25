from model.Simulator import Simulator
from model.Deck import Deck
from model.Card import Card
from model.Suit import Suit
from model.Rank import Rank

def main() -> None:
    deck = Deck()
    deck.shuffle()

    hand = deck.deal(2)
    #hand = [Card(14,Suit.SPADES), Card(14, Suit.HEARTS)]

    print("hand:")
    for card in hand:
        print(card.display())

    for trials_done, equity in Simulator.simulate_equity(hand, 100_000):
        if trials_done % 1000 == 0:
            print(f"\r{trials_done}: equity = {equity:.4f}", end="", flush=True)

if __name__ == "__main__":
    main()