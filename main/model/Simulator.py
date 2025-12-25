from .Evaluator import Evaluator
from .Card import Card
from .Deck import Deck

class Simulator:
    @staticmethod
    def simulate_equity(hand: list[Card], trials: int = 100000) -> float:
        wins = 0
        ties = 0

        for trial in range(trials):
            deck = Deck()
            deck.shuffle()
            deck.removeCards(hand[0], hand[1])

            villain_hand = [deck.draw(), deck.draw()]

            board = deck.deal(5)

            hero_best = Evaluator.best_hand(hand + board)
            villain_best = Evaluator.best_hand(villain_hand + board)

            result = Evaluator.compare_hands(hero_best, villain_best)

            if result == 1:
                wins += 1
            elif result == 0:
                ties += 1

            equity = (wins + 0.5*ties) / (trial + 1)
            yield trial + 1, equity