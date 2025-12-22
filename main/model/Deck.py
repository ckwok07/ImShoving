from model.Card import Card
from model.Rank import Rank
from model.Suit import Suit
import random

class Deck:
    def __init__(self) -> None:
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop()