from .Suit import Suit
from .Rank import Rank


# A class to represent a standard playing card with a suit and a rank
class Card:
    # constructor, allowing for the creation of card with Card(14, 3) or Card(Rank.ACE, Suit.SPADES)
    def __init__(self, rank, suit) -> None:
        self.rank = rank.value if hasattr(rank, "value") else rank

        self.suit = suit.value if hasattr(suit, "value") else suit

    # displays a card's rank and suit
    def display(self) -> str:
        rank_str = Rank(self.rank).display()
        suit_str = Suit(self.suit).display()
        return rank_str + suit_str
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit