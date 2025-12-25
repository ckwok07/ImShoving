from model.Simulator import Simulator
from model.Deck import Deck
from model.Card import Card
from model.Suit import Suit
from model.Rank import Rank

def main() -> None:
    deck = Deck()
    deck.shuffle()

    #hand = deck.deal(2)
    hand = [Card(14,Suit.SPADES), Card(14, Suit.HEARTS)]

    print("hand:")
    for card in hand:
        print(card.display())

    for trials, winrate, tierate, equity in Simulator.simulate_equity(hand, 100_000):
            if trials % 500 == 0:
                print(
                    f"\rtrials:{trials:6d} | "
                    f"win={winrate:.4f} "
                    f"tie={tierate:.4f} "
                    f"equity={equity:.4f}",
                    end="",
                    flush=True
                )

if __name__ == "__main__":
    main()