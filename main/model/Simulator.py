from collections.abc import Iterator
from .Evaluator import Evaluator
from .Card import Card
from .Deck import Deck

class Simulator:
    @staticmethod
    def simulate_equity(hand: list[Card], board: list[Card] | None = None, trials: int = 100000) -> Iterator[tuple[int, float, float, float]]:
        wins = 0
        ties = 0

        if board is None:
            board = []

        missing_board = 5 - len(board)
        assert 0 <= missing_board <= 5

        for trial in range(trials):
            deck = Deck()
            deck.shuffle()
            deck.removeCards(hand + board)

            villain_hand = [deck.draw(), deck.draw()]
            rest_of_board = deck.deal(missing_board)

            full_board = board + rest_of_board

            hero_best = Evaluator.best_hand(hand + full_board)
            villain_best = Evaluator.best_hand(villain_hand + full_board)

            result = Evaluator.compare_hands(hero_best, villain_best)

            if result == 1:
                wins += 1
            elif result == 0:
                ties += 1

            winrate = wins/ (trial + 1)
            tierate = ties/ (trial + 1)
            equity = (wins + 0.5*ties) / (trial + 1)
            yield trial + 1, winrate, tierate, equity