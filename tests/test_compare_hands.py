from random import random
from main.model.Card import Card
from main.model.Suit import Suit
from main.model.Deck import Deck
from main.model.Evaluator import Evaluator

def test_hand_order():
    hand1 = [
        Card(14, 0), 
        Card(13, 1), 
        Card(12, 2), 
        Card(11, 3), 
        Card(9, 0)
    ]

    hand2 = list(reversed(hand1))

    assert Evaluator.compare_hands(hand1, hand2) == 0

def test_high_card_vs_high_card():
    hand1 = [
        Card(14, Suit.SPADES),
        Card(13, Suit.HEARTS),
        Card(11, Suit.DIAMONDS),
        Card(9, Suit.CLUBS),
        Card(2, Suit.SPADES)
    ]

    hand2 = [
        Card(3, Suit.SPADES),
        Card(13, Suit.HEARTS),
        Card(11, Suit.DIAMONDS),
        Card(9, Suit.CLUBS),
        Card(2, Suit.SPADES)
    ]
    assert Evaluator.compare_hands(hand1, hand2) == 1

def test_high_card_vs_high_card_ordering():
    hand1 = [
        Card(13, Suit.HEARTS),
        Card(11, Suit.DIAMONDS),
        Card(9, Suit.CLUBS),
        Card(2, Suit.SPADES),
        Card(14, Suit.SPADES)
    ]

    hand2 = [
        Card(3, Suit.SPADES),
        Card(2, Suit.HEARTS),
        Card(11, Suit.DIAMONDS),
        Card(9, Suit.CLUBS),
        Card(13, Suit.SPADES)
    ]
    assert Evaluator.compare_hands(hand1, hand2) == 1

def test_royal_vs_quad_aces():
    hand1 = [
        Card(14, Suit.HEARTS),
        Card(14, Suit.DIAMONDS),
        Card(14, Suit.CLUBS),
        Card(14, Suit.SPADES),
        Card(13, Suit.SPADES)
    ]

    hand2 = [
        Card(14, Suit.HEARTS),
        Card(12, Suit.HEARTS),
        Card(11, Suit.HEARTS),
        Card(10, Suit.HEARTS),
        Card(13, Suit.HEARTS)
    ]
    assert Evaluator.compare_hands(hand1, hand2) == -1

def test_same_hand():
    hand1 = [
        Card(2, Suit.DIAMONDS),
        Card(2, Suit.HEARTS),
        Card(8, Suit.CLUBS),
        Card(8, Suit.SPADES),
        Card(13, Suit.CLUBS),
    ]

    hand2 = [
        Card(2, Suit.DIAMONDS),
        Card(2, Suit.HEARTS),
        Card(8, Suit.CLUBS),
        Card(8, Suit.SPADES),
        Card(13, Suit.CLUBS),
    ]

    assert Evaluator.compare_hands(hand1, hand2) == 0

    def test_same_hand_suits():
        hand1 = [
            Card(2, Suit.DIAMONDS),
            Card(2, Suit.HEARTS),
            Card(8, Suit.CLUBS),
            Card(8, Suit.SPADES),
            Card(13, Suit.CLUBS),
        ]

        hand2 = [
            Card(2, Suit.SPADES),
            Card(2, Suit.HEARTS),
            Card(8, Suit.CLUBS),
            Card(8, Suit.HEARTS),
            Card(13, Suit.CLUBS),
        ]

        assert Evaluator.compare_hands(hand1, hand2) == 0

def test_compare_hands_antisymmetric():
    h1 = [Card(14,0), Card(13,1), Card(11,2), Card(9,3), Card(2,0)]
    h2 = [Card(13,0), Card(12,1), Card(11,2), Card(9,3), Card(2,0)]

    assert Evaluator.compare_hands(h1, h2) == 1
    assert Evaluator.compare_hands(h2, h1) == -1

def test_compare_equal_hands():
    h1 = [Card(14,0), Card(13,1), Card(12,2), Card(11,3), Card(9,0)]
    h2 = [Card(9,0), Card(11,3), Card(12,2), Card(13,1), Card(14,0)]

    assert Evaluator.compare_hands(h1, h2) == 0

