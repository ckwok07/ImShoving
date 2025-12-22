from enum import Enum

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def display(self) -> str:
        if self.value < 10:
            return str(self.value)
        return {
            10: "T",
            11: "J",
            12: "Q",
            13: "K",
            14: "A",} [self.value]