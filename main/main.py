from model.Simulator import Simulator
from model.Deck import Deck
from model.Card import Card
from model.Suit import Suit
from model.Rank import Rank
from model.Range import Range
from model.Handbuilder import Handbuilder
from model.Evaluator import Evaluator

def main() -> None:
    deck = Deck()
    deck.shuffle()
    board = []

    # hands = Handbuilder.suited_hands()
    # for hand in hands:
    #     for card in hand:
    #         print(card.display())

    #hand = deck.deal(2)
    hand = [Card(13,Suit.HEARTS), Card(5, Suit.HEARTS)]
    board = [Card(12, Suit.SPADES), Card(8, Suit.HEARTS), Card(5, Suit.SPADES), Card(7, Suit.HEARTS), Card(9, Suit.SPADES)]
    #board = [Card(12,Suit.SPADES), Card(10,Suit.SPADES), Card(9,Suit.DIAMONDS)]

    print("hand:", " ".join(card.display() for card in hand))
    print("board:", " ".join(card.display() for card in board))

    equity = Simulator.simulate_equity(hand,board,2,100000)
    print(equity)
    # ev = Simulator.simulate_call_ev(1,1,equity)
    # print(ev)



    # finalEquity = 0
    # for trials, equity, std, ci95 in Simulator.simulate_equity(hand, board, 2, 30000):
    #     if trials % 500 == 0:
    #         print(
    #             f"\rtrials:{trials:6d} | "
    #             f"equity={equity:.4f}",
    #             f"std={std:.4f}",
    #             f"ci95={ci95:.4f}",
    #             end="",
    #             flush=True)
    #     finalEquity = equity
    # print()
    # print(f"EV = {Simulator.simulate_call_ev(10, 5, finalEquity)}")


    # TT_plus = Range(Handbuilder.pocket_pairs(10))

    # print(Simulator.simulate_call_ev(10, 5, hand, board, 2, 30000))
    # print(Simulator.simulate_call_ev_range(10, 5, hand, board, 2, [TT_plus], 30000))


    # for trials, equity, std, ci95 in Simulator.simulate_equity_in_range(hand, board, 2, [TT_plus], 100000):
    #     if trials % 500 == 0:
    #         print(
    #             f"\rtrials:{trials:6d} | "
    #             f"equity={equity:.4f}",
    #             f"std={std:.4f}",
    #             f"ci95={ci95:.4f}",
    #             end="",
    #             flush=True)
    #     finalEquity = equity
    # print()
    # print(f"EV = {Simulator.simulate_call_ev(10, 5, finalEquity)}")


if __name__ == "__main__":
    main()