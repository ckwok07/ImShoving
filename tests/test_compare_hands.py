from random import random
from main.model.Card import Card
from main.model.Suit import Suit
from main.model.Deck import Deck
from main.model.Evaluator import Evaluator

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