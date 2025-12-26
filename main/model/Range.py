from .Card import Card
from .Deck import Deck
import random

class Range:
    ALL_HANDS: list[list[Card]] | None = None
    @staticmethod
    def generateHands() -> list[list[Card]]:
        deck = Deck()
        cards = deck.cards
        hands = []

        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                hands.append([cards[i], cards[j]])

        return hands


    def __init__(self, hands: list[list[Card]] | None = None) -> None:
        if Range.ALL_HANDS is None:
            Range.ALL_HANDS = Range.generateHands()
        if hands == None:
            self.hands = Range.ALL_HANDS
        else:
            self.hands = hands

    def is_blocked(self, hand: list[Card], known: list[Card]) -> bool:
        for card1 in hand:
            for card2 in known:
                if card1.rank == card2.rank and card1.suit == card2.suit:
                    return True
        return False
    
    def available_hands(self, known: list[Card]) -> list[list[Card]]:
        available_hands = []

        for hand in self.hands:
            if not self.is_blocked(hand, known):
                available_hands.append(hand)
        
        return available_hands
    
    def sample_hand(self, known: list[Card]) -> list[Card]:
        possible_hands = self.available_hands(known)
        assert possible_hands #check if a hand in the range exists
        return random.choice(possible_hands)