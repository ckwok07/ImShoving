from .Card import Card
from .Rank import Rank
from .Suit import Suit

from itertools import combinations


class Handbuilder:

    # return true if hand is a pocket pair
    @staticmethod
    def pair(hand: list[Card]) -> bool:
        assert len(hand) == 2

        return hand[0].rank == hand[1].rank

    # return true if hand is suited
    @staticmethod
    def suited(hand: list[Card]) -> bool:
        assert len(hand) == 2

        return hand[0].suit == hand[1].suit
    
    # return true if hand is connected
    @staticmethod
    def connected(hand: list[Card]) -> bool:
        assert len(hand) == 2

        return (abs(hand[0].rank - hand[1].rank) == 1 or 
                (hand[0].rank == 2 and hand[1].rank == 14) or 
                (hand[1].rank == 2 and hand[0].rank == 14))
    
    # return combinations of all pocket pairs >= min_rank
    @staticmethod
    def pocket_pairs(min_rank: int) -> list[list[Card]]:
        hands = []

        for rank in range(min_rank, 15):
            for s1, s2 in combinations(Suit, 2):
                hand = [Card(rank, s1), Card(rank, s2)]
                assert Handbuilder.pair(hand)
                hands.append(hand)

        return hands
        
    
