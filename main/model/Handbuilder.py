from .Card import Card
from .Rank import Rank
from .Suit import Suit
from .Range import Range

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
    
    # return true if hand is suited and connected
    @staticmethod
    def suited_connected(hand: list[Card]) -> bool:
        assert len(hand) == 2
        return (Handbuilder.suited(hand) and Handbuilder.connected(hand))
    
    # return combinations of all pocket pairs >= min_rank
    @staticmethod
    def pocket_pairs(min_rank: int) -> list[list[Card]]:
        hands = []

        if Range.ALL_HANDS is None:
            Range.ALL_HANDS = Range.generateHands()

        for hand in Range.ALL_HANDS:
            if Handbuilder.pair(hand) and hand[0].rank >= min_rank:
                hands.append(hand)

        return hands
    
    # return combinations of all suited and connected hands
    @staticmethod
    def suited_connected_hands() -> list[list[Card]]:
        hands = []

        if Range.ALL_HANDS is None:
            Range.ALL_HANDS = Range.generateHands()

        for hand in Range.ALL_HANDS:
            if Handbuilder.suited_connected(hand):
                hands.append(hand)
                
        return hands
    
    # return combinations of all suited hands
    @staticmethod
    def suited_hands() -> list[list[Card]]:
        hands = []

        if Range.ALL_HANDS is None:
            Range.ALL_HANDS = Range.generateHands()

        for hand in Range.ALL_HANDS:
            if Handbuilder.suited(hand):
                hands.append(hand)
                
        return hands