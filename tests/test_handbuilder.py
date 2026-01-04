
import pytest
from main.model.Card import Card
from main.model.Suit import Suit
from main.model.Handbuilder import Handbuilder

def test_pair():
    hand = [Card(14, 1), Card(14, 0)]

    assert Handbuilder.connected(hand) == False
    assert Handbuilder.pair(hand) == True
    assert Handbuilder.suited(hand) == False

def test_connected():
    hand1 = [Card(14,1), Card(13,1)]
    hand2 = [Card(13,1), Card(14,1)]
    hand3 = [Card(12,1), Card(14,1)]
    hand4 = [Card(14,1), Card(2,1)]
    hand5 = [Card(2,1), Card(14,2)]

    assert Handbuilder.connected(hand1) == True
    assert Handbuilder.connected(hand2) == True
    assert Handbuilder.connected(hand3) == False
    assert Handbuilder.connected(hand4) == True
    assert Handbuilder.connected(hand5) == True

def test_pocket_pairs():
    TT_actual = [[Card(10, Suit.DIAMONDS), Card(10, Suit.CLUBS)], 
                [Card(10, Suit.DIAMONDS), Card(10, Suit.HEARTS)],
                [Card(10, Suit.DIAMONDS), Card(10, Suit.SPADES)],

                [Card(11, Suit.DIAMONDS), Card(11, Suit.CLUBS)],
                [Card(11, Suit.DIAMONDS), Card(11, Suit.HEARTS)],
                [Card(11, Suit.DIAMONDS), Card(11, Suit.SPADES)],

                [Card(12, Suit.DIAMONDS), Card(12, Suit.CLUBS)],
                [Card(12, Suit.DIAMONDS), Card(12, Suit.HEARTS)],
                [Card(12, Suit.DIAMONDS), Card(12, Suit.SPADES)],

                [Card(13, Suit.DIAMONDS), Card(13, Suit.CLUBS)],
                [Card(13, Suit.DIAMONDS), Card(13, Suit.HEARTS)],
                [Card(13, Suit.DIAMONDS), Card(13, Suit.SPADES)],

                [Card(14, Suit.DIAMONDS), Card(14, Suit.CLUBS)],
                [Card(14, Suit.DIAMONDS), Card(14, Suit.HEARTS)],
                [Card(14, Suit.DIAMONDS), Card(14, Suit.SPADES)],

                [Card(10, Suit.CLUBS), Card(10, Suit.HEARTS)],
                [Card(10, Suit.CLUBS), Card(10, Suit.SPADES)],

                [Card(11, Suit.CLUBS), Card(11, Suit.HEARTS)],
                [Card(11, Suit.CLUBS), Card(11, Suit.SPADES)],

                [Card(12, Suit.CLUBS), Card(12, Suit.HEARTS)],
                [Card(12, Suit.CLUBS), Card(12, Suit.SPADES)],

                [Card(13, Suit.CLUBS), Card(13, Suit.HEARTS)],
                [Card(13, Suit.CLUBS), Card(13, Suit.SPADES)],

                [Card(14, Suit.CLUBS), Card(14, Suit.HEARTS)],
                [Card(14, Suit.CLUBS), Card(14, Suit.SPADES)],

                [Card(10, Suit.HEARTS), Card(10, Suit.SPADES)],
                [Card(11, Suit.HEARTS), Card(11, Suit.SPADES)],
                [Card(12, Suit.HEARTS), Card(12, Suit.SPADES)],
                [Card(13, Suit.HEARTS), Card(13, Suit.SPADES)],
                [Card(14, Suit.HEARTS), Card(14, Suit.SPADES)]]

    TT = Handbuilder.pocket_pairs(10)

    assert TT_actual == TT