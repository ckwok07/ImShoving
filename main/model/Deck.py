from main.model import Card, Rank, Suit

class Deck:
    def __init__(self):
        self.deck = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))