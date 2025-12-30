from .Card import Card
from .Deck import Deck
import random

# A class to represent a players range of cards.
class Range:
    
    # return all possible hands (52 choose 2) = 1326 hands
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
        if hands is None:
            self.hands = Range.ALL_HANDS
        else:
            self.hands = hands

    # return true if hand contains any card from known, false otherwise
    def is_blocked(self, hand: list[Card], known: list[Card]) -> bool:
        for card1 in hand:
            for card2 in known:
                if card1.rank == card2.rank and card1.suit == card2.suit:
                    return True
        return False
    
    # return all hands excluding those that have any card from known
    def available_hands(self, known: list[Card]) -> list[list[Card]]:
        available_hands = []

        for hand in self.hands:
            if not self.is_blocked(hand, known):
                available_hands.append(hand)
        
        return available_hands
    
    # return a random hand that is available
    def sample_hand(self, known: list[Card]) -> list[Card]:
        possible_hands = self.available_hands(known)
        assert possible_hands #check if a hand in the range exists
        return random.choice(possible_hands)