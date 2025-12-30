from model.Simulator import Simulator
from model.Deck import Deck
from model.Card import Card
from model.Suit import Suit
from model.Rank import Rank
from model.Range import Range

def main() -> None:
    deck = Deck()
    deck.shuffle()
    board = []

    #hand = deck.deal(2)
    hand = [Card(14,Suit.SPADES), Card(11, Suit.SPADES)]
    #board = deck.deal(3)
    board = [Card(12,Suit.SPADES), Card(10,Suit.SPADES), Card(9,Suit.DIAMONDS)]

    print("hand:")
    for card in hand:
        print(card.display())
    print("board:")
    for card in board:
        print(card.display())
    
    for trials, equity, std, ci95 in Simulator.simulate_equity(hand, board, 2, 30000):
        if trials % 500 == 0:
            print(
                f"\rtrials:{trials:6d} | "
                f"equity={equity:.4f}",
                f"std={std:.4f}",
                f"ci95={ci95:.4f}",
                end="",
                flush=True
            )
    print()


    TT_plus = Range([
        # TT
        [Card(10, Suit.SPADES),   Card(10, Suit.HEARTS)],
        [Card(10, Suit.SPADES),   Card(10, Suit.DIAMONDS)],
        [Card(10, Suit.SPADES),   Card(10, Suit.CLUBS)],
        [Card(10, Suit.HEARTS),   Card(10, Suit.DIAMONDS)],
        [Card(10, Suit.HEARTS),   Card(10, Suit.CLUBS)],
        [Card(10, Suit.DIAMONDS), Card(10, Suit.CLUBS)],

        # JJ
        [Card(11, Suit.SPADES),   Card(11, Suit.HEARTS)],
        [Card(11, Suit.SPADES),   Card(11, Suit.DIAMONDS)],
        [Card(11, Suit.SPADES),   Card(11, Suit.CLUBS)],
        [Card(11, Suit.HEARTS),   Card(11, Suit.DIAMONDS)],
        [Card(11, Suit.HEARTS),   Card(11, Suit.CLUBS)],
        [Card(11, Suit.DIAMONDS), Card(11, Suit.CLUBS)],

        # QQ
        [Card(12, Suit.SPADES),   Card(12, Suit.HEARTS)],
        [Card(12, Suit.SPADES),   Card(12, Suit.DIAMONDS)],
        [Card(12, Suit.SPADES),   Card(12, Suit.CLUBS)],
        [Card(12, Suit.HEARTS),   Card(12, Suit.DIAMONDS)],
        [Card(12, Suit.HEARTS),   Card(12, Suit.CLUBS)],
        [Card(12, Suit.DIAMONDS), Card(12, Suit.CLUBS)],

        # KK
        [Card(13, Suit.SPADES),   Card(13, Suit.HEARTS)],
        [Card(13, Suit.SPADES),   Card(13, Suit.DIAMONDS)],
        [Card(13, Suit.SPADES),   Card(13, Suit.CLUBS)],
        [Card(13, Suit.HEARTS),   Card(13, Suit.DIAMONDS)],
        [Card(13, Suit.HEARTS),   Card(13, Suit.CLUBS)],
        [Card(13, Suit.DIAMONDS), Card(13, Suit.CLUBS)],

        # AA
        [Card(14, Suit.SPADES),   Card(14, Suit.HEARTS)],
        [Card(14, Suit.SPADES),   Card(14, Suit.DIAMONDS)],
        [Card(14, Suit.SPADES),   Card(14, Suit.CLUBS)],
        [Card(14, Suit.HEARTS),   Card(14, Suit.DIAMONDS)],
        [Card(14, Suit.HEARTS),   Card(14, Suit.CLUBS)],
        [Card(14, Suit.DIAMONDS), Card(14, Suit.CLUBS)],
    ])


    for trials, equity, std, ci95 in Simulator.simulate_equity_in_range(hand, board, 2, [TT_plus], 30000):
        if trials % 500 == 0:
            print(
                f"\rtrials:{trials:6d} | "
                f"equity={equity:.4f}",
                f"std={std:.4f}",
                f"ci95={ci95:.4f}",
                end="",
                flush=True
            )
    print()

if __name__ == "__main__":
    main()