from random import random
from main.model.Card import Card
from main.model.Suit import Suit
from main.model.Deck import Deck
from main.model.Evaluator import Evaluator
import random
from itertools import combinations

def test_best_hand_over_200_trials():
    for _ in range(200):  # number of trials
        deck = Deck()
        deck.shuffle()
        cards = [deck.draw() for _ in range(7)]

        best = Evaluator.best_hand(cards)
        best_score = Evaluator.mapper(best)

        for hand in combinations(cards, 5):
            assert best_score >= Evaluator.mapper(hand)


def test_straight():
    cards = [
        Card(14, Suit.SPADES),
        Card(2, Suit.CLUBS),
        Card(3, Suit.HEARTS),
        Card(4, Suit.SPADES),
        Card(5, Suit.CLUBS),
        Card(14, Suit.DIAMONDS),
        Card(14, Suit.HEARTS)
    ]

    hand = Evaluator.best_hand(cards)
    expected_hand = [Card(14, Suit.SPADES),
                    Card(2, Suit.CLUBS),
                    Card(3, Suit.HEARTS),
                    Card(4, Suit.SPADES),
                    Card(5, Suit.CLUBS)
                ]
    assert Evaluator.mapper(hand) == Evaluator.mapper(expected_hand)
    assert Evaluator.compare_hands(hand,expected_hand) == 0

def test_one_pair():
    cards = [
        Card(9, Suit.SPADES),
        Card(9, Suit.HEARTS),
        Card(14, Suit.CLUBS),
        Card(13, Suit.DIAMONDS),
        Card(11, Suit.SPADES),
        Card(4, Suit.CLUBS),
        Card(2, Suit.HEARTS)
    ]

    hand = Evaluator.best_hand(cards)

    expected_hand = [
        Card(9, Suit.SPADES),
        Card(9, Suit.HEARTS),
        Card(14, Suit.CLUBS),
        Card(13, Suit.DIAMONDS),
        Card(11, Suit.SPADES)
    ]

    assert Evaluator.mapper(hand) == Evaluator.mapper(expected_hand)
    assert Evaluator.compare_hands(hand, expected_hand) == 0

def test_two_pair():
    cards = [
        Card(10, Suit.SPADES),
        Card(10, Suit.HEARTS),
        Card(7, Suit.CLUBS),
        Card(7, Suit.DIAMONDS),
        Card(14, Suit.SPADES),
        Card(4, Suit.HEARTS),
        Card(2, Suit.CLUBS)
    ]

    hand = Evaluator.best_hand(cards)

    expected_hand = [
        Card(10, Suit.SPADES),
        Card(10, Suit.HEARTS),
        Card(7, Suit.CLUBS),
        Card(7, Suit.DIAMONDS),
        Card(14, Suit.SPADES)
    ]

    assert Evaluator.mapper(hand) == Evaluator.mapper(expected_hand)
    assert Evaluator.compare_hands(hand, expected_hand) == 0

def test_three_of_a_kind():
    cards = [
        Card(8, Suit.SPADES),
        Card(8, Suit.HEARTS),
        Card(8, Suit.DIAMONDS),
        Card(14, Suit.CLUBS),
        Card(13, Suit.SPADES),
        Card(4, Suit.CLUBS),
        Card(2, Suit.HEARTS)
    ]

    hand = Evaluator.best_hand(cards)

    expected_hand = [
        Card(8, Suit.SPADES),
        Card(8, Suit.HEARTS),
        Card(8, Suit.DIAMONDS),
        Card(14, Suit.CLUBS),
        Card(13, Suit.SPADES)
    ]

    assert Evaluator.mapper(hand) == Evaluator.mapper(expected_hand)
    assert Evaluator.compare_hands(hand, expected_hand) == 0

def test_full_house():
    cards = [
        Card(6, Suit.SPADES),
        Card(6, Suit.HEARTS),
        Card(6, Suit.DIAMONDS),
        Card(12, Suit.CLUBS),
        Card(12, Suit.SPADES),
        Card(9, Suit.HEARTS),
        Card(2, Suit.CLUBS)
    ]

    hand = Evaluator.best_hand(cards)

    expected_hand = [
        Card(6, Suit.SPADES),
        Card(6, Suit.HEARTS),
        Card(6, Suit.DIAMONDS),
        Card(12, Suit.CLUBS),
        Card(12, Suit.SPADES)
    ]

    assert Evaluator.mapper(hand) == Evaluator.mapper(expected_hand)
    assert Evaluator.compare_hands(hand, expected_hand) == 0

def test_flush():
    cards = [
        Card(14, Suit.HEARTS),
        Card(12, Suit.HEARTS),
        Card(10, Suit.HEARTS),
        Card(8, Suit.HEARTS),
        Card(3, Suit.HEARTS),
        Card(9, Suit.CLUBS),
        Card(2, Suit.SPADES)
    ]

    hand = Evaluator.best_hand(cards)

    expected_hand = [
        Card(14, Suit.HEARTS),
        Card(12, Suit.HEARTS),
        Card(10, Suit.HEARTS),
        Card(8, Suit.HEARTS),
        Card(3, Suit.HEARTS)
    ]

    assert Evaluator.mapper(hand) == Evaluator.mapper(expected_hand)
    assert Evaluator.compare_hands(hand, expected_hand) == 0

def test_straight_flush():
    cards = [
        Card(9, Suit.SPADES),
        Card(10, Suit.SPADES),
        Card(11, Suit.SPADES),
        Card(12, Suit.SPADES),
        Card(13, Suit.SPADES),
        Card(2, Suit.HEARTS),
        Card(4, Suit.CLUBS)
    ]

    hand = Evaluator.best_hand(cards)

    expected_hand = [
        Card(9, Suit.SPADES),
        Card(10, Suit.SPADES),
        Card(11, Suit.SPADES),
        Card(12, Suit.SPADES),
        Card(13, Suit.SPADES)
    ]

    assert Evaluator.mapper(hand) == Evaluator.mapper(expected_hand)
    assert Evaluator.compare_hands(hand, expected_hand) == 0

def test_best_hand_order_invariant():
    cards = [
        Card(14,0), Card(14,1), Card(13,2),
        Card(12,3), Card(11,0), Card(9,1), Card(2,2)
    ]

    h1 = Evaluator.best_hand(cards)
    cards.reverse()
    h2 = Evaluator.best_hand(cards)

    assert Evaluator.compare_hands(h1, h2) == 0

def test_best_hand_identity():
    cards = [Card(14,0), Card(13,1), Card(12,2), Card(11,3), Card(9,0)]
    assert Evaluator.mapper(Evaluator.best_hand(cards)) == Evaluator.mapper(cards)

def test_best_2fullhouses():
    cards = [
        Card(10,0), Card(10,1), Card(10,2),
        Card(8,0), Card(8,1), Card(8,2),
        Card(2,3)
    ]

    best = Evaluator.best_hand(cards)
    assert Evaluator.mapper(best)[0] == 6  # full house
    assert Evaluator.mapper(best) == (6, 10, 8, 0, 0, 0)

def test_best_2fullhouses_order():
    cards = [
        Card(8,0), Card(10,1), Card(10,2),
        Card(10,0), Card(8,1), Card(8,2),
        Card(2,3)
    ]

    best = Evaluator.best_hand(cards)
    assert Evaluator.mapper(best)[0] == 6  # full house
    assert Evaluator.mapper(best) == (6, 10, 8, 0, 0, 0)

def test_best_hand_flush_over_straight():
    cards = [
        Card(14, 1), Card(12, 1), Card(10, 1), Card(7, 1), Card(3, 1),  # flush
        Card(9, 0), Card(8, 2)                                         # straight exists
    ]

    best = Evaluator.best_hand(cards)

    assert Evaluator.mapper(best) == (5, 14, 12, 10, 7, 3)

def test_best_hand_two_flushes():
    cards = [
        Card(14, 0), Card(11, 0), Card(9, 0), Card(6, 0), Card(2, 0),  # A-high flush
        Card(13, 1), Card(12, 1)
    ]

    best = Evaluator.best_hand(cards)

    assert Evaluator.mapper(best) == (5, 14, 11, 9, 6, 2)

def test_best_hand_two_straights():
    cards = [
        Card(5, 0), Card(6, 1), Card(7, 2), Card(8, 3), Card(9, 0),   # 9-high
        Card(10, 1), Card(11, 2)                                     # enables J-high
    ]

    best = Evaluator.best_hand(cards)

    # J-high straight
    assert Evaluator.mapper(best) == (4, 11, 0, 0, 0, 0)



