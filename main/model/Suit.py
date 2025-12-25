from enum import Enum

class Suit(Enum):
    DIAMONDS = 0
    CLUBS = 1
    HEARTS = 2
    SPADES = 3

    def display(self) -> str:
        return {
            Suit.CLUBS: "c",
            Suit.DIAMONDS: "d",
            Suit.HEARTS: "h",
            Suit.SPADES: "s"}[self]  