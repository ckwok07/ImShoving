from collections.abc import Iterator
from .Evaluator import Evaluator
from .Card import Card
from .Deck import Deck
from .Range import Range

# A class to simulate poker runouts
class Simulator:
    # given a hand, board, num players, and x trials, return percentage of showdowns won after x simulations
    @staticmethod
    def simulate_equity(hand: list[Card], 
                        board: list[Card] | None = None,
                        players: int = 2, 
                        trials: int = 100000) -> Iterator[tuple[int, float]]:
        assert 2 <= players <= 6
        assert len(hand) == 2

        if board is None:
            board = []

        missing_board = 5 - len(board)
        assert 0 <= missing_board <= 5

        equity_sum = 0.0

        for trial in range(trials):
            assert len(set((c.rank, c.suit) for c in hand + board)) == len(hand + board)
            
            deck = Deck()
            deck.shuffle()
            deck.removeCards(hand + board)

            villains = []
            for num in range(players - 1):
                villains.append([deck.draw(), deck.draw()])

            rest_of_board = deck.deal(missing_board)

            full_board = board + rest_of_board

            hero_eval = Evaluator.mapper(Evaluator.best_hand(hand + full_board))
            
            villain_evals = []
            for v in villains:
                best = Evaluator.best_hand(v + full_board)
                villain_evals.append(Evaluator.mapper(best))

            all_evals = [hero_eval] + villain_evals
            best_eval = max(all_evals)

            if hero_eval == best_eval:
                tied = sum(1 for e in all_evals if e == best_eval)
                equity_sum += 1.0 / tied

            yield trial + 1, equity_sum / (trial + 1)

    # given a hand, board, num players, list of ranges and x trials, 
    # return percentage of showdowns won after x simulations with players with given ranges
    @staticmethod
    def simulate_equity_in_range(hand: list[Card],
                                 board: list[Card] | None = None,
                                 players: int = 2,
                                 villianRanges: list[Range] | None = None,
                                 trials: int = 100000) -> Iterator[tuple[int, float]]:
        if villianRanges is None:
            villianRanges = []

        assert 2 <= players <= 6
        assert len(hand) == 2
        assert len(villianRanges) <= players - 1

        if len(villianRanges) < players - 1:
            for i in range((players - 1) - len(villianRanges)):
                villianRanges.append(Range())

        if board is None:
            board = []
        
        missing_board = 5 - len(board)
        assert 0 <= missing_board <= 5

        equity_sum = 0.0

        for trial in range(trials):
            deck = Deck()
            deck.shuffle()
            deck.removeCards(hand + board)

            villains = []
            known = hand + board
            for num in range(players - 1):
                vRange = villianRanges[num]
                v_hand = vRange.sample_hand(known)
                villains.append(v_hand)
                known += v_hand
                deck.removeCards(v_hand)
            
            rest_of_board = deck.deal(missing_board)
            full_board = board + rest_of_board
            hero_eval = Evaluator.mapper(Evaluator.best_hand(hand + full_board))

            villain_evals = []
            for v in villains:
                best = Evaluator.best_hand(v + full_board)
                villain_evals.append(Evaluator.mapper(best))

            all_evals = [hero_eval] + villain_evals
            best_eval = max(all_evals)

            if hero_eval == best_eval:
                tied = sum(1 for e in all_evals if e == best_eval)
                equity_sum += 1.0 / tied

            yield trial + 1, equity_sum / (trial + 1)