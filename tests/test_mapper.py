from main.model.Card import Card
from main.model.Suit import Suit
from main.model.Evaluator import Evaluator

def test_category():
    high = [Card(14,0), Card(11,1), Card(9,2), Card(6,3), Card(2,0)]
    pair = [Card(10,0), Card(10,1), Card(9,2), Card(6,3), Card(2,0)]
    trips = [Card(8,0), Card(8,1), Card(8,2), Card(6,3), Card(2,0)]

    assert Evaluator.mapper(trips) > Evaluator.mapper(pair)
    assert Evaluator.mapper(pair) > Evaluator.mapper(high)


def test_high_card():
    hand = [
        Card(14, Suit.SPADES),
        Card(13, Suit.HEARTS),
        Card(11, Suit.DIAMONDS),
        Card(9, Suit.CLUBS),
        Card(2, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (0, 14, 13, 11, 9, 2)


def test_high_card_order():
    hand = [
        Card(14, Suit.HEARTS),
        Card(13, Suit.DIAMONDS),
        Card(11, Suit.CLUBS),
        Card(8, Suit.SPADES),
        Card(3, Suit.HEARTS),
    ]
    assert Evaluator.mapper(hand) == (0, 14, 13, 11, 8, 3)


def test_pair():
    hand = [
        Card(8, Suit.SPADES),
        Card(8, Suit.DIAMONDS),
        Card(14, Suit.HEARTS),
        Card(12, Suit.CLUBS),
        Card(2, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (1, 8, 14, 12, 2, 0)


def test_pair_kickers():
    hand = [
        Card(5, Suit.SPADES),
        Card(5, Suit.DIAMONDS),
        Card(14, Suit.HEARTS),
        Card(9, Suit.CLUBS),
        Card(3, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (1, 5, 14, 9, 3, 0)


def test_two_pair():
    hand = [
        Card(13, Suit.SPADES),
        Card(13, Suit.DIAMONDS),
        Card(10, Suit.HEARTS),
        Card(10, Suit.CLUBS),
        Card(14, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (2, 13, 10, 14, 0, 0)


def test_two_pair_kicker():
    hand = [
        Card(12, Suit.SPADES),
        Card(12, Suit.DIAMONDS),
        Card(9, Suit.HEARTS),
        Card(9, Suit.CLUBS),
        Card(13, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (2, 12, 9, 13, 0, 0)


def test_set():
    hand = [
        Card(7, Suit.SPADES),
        Card(7, Suit.DIAMONDS),
        Card(7, Suit.HEARTS),
        Card(14, Suit.CLUBS),
        Card(9, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (3, 7, 14, 9, 0, 0)


def test_set_kickers():
    hand = [
        Card(6, Suit.SPADES),
        Card(6, Suit.DIAMONDS),
        Card(6, Suit.HEARTS),
        Card(13, Suit.CLUBS),
        Card(2, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (3, 6, 13, 2, 0, 0)


def test_straight():
    hand = [
        Card(9, Suit.SPADES),
        Card(8, Suit.DIAMONDS),
        Card(7, Suit.HEARTS),
        Card(6, Suit.CLUBS),
        Card(5, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (4, 9, 0, 0, 0, 0)


def test_wheel_straight():
    hand = [
        Card(14, Suit.SPADES),
        Card(2, Suit.DIAMONDS),
        Card(3, Suit.HEARTS),
        Card(4, Suit.CLUBS),
        Card(5, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (4, 5, 0, 0, 0, 0)


def test_flush():
    hand = [
        Card(14, Suit.SPADES),
        Card(11, Suit.SPADES),
        Card(9, Suit.SPADES),
        Card(6, Suit.SPADES),
        Card(3, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (5, 14, 11, 9, 6, 3)


def test_flush_kickers():
    hand = [
        Card(13, Suit.HEARTS),
        Card(12, Suit.HEARTS),
        Card(10, Suit.HEARTS),
        Card(8, Suit.HEARTS),
        Card(2, Suit.HEARTS),
    ]
    assert Evaluator.mapper(hand) == (5, 13, 12, 10, 8, 2)


def test_full_house():
    hand = [
        Card(10, Suit.SPADES),
        Card(10, Suit.DIAMONDS),
        Card(10, Suit.HEARTS),
        Card(2, Suit.CLUBS),
        Card(2, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (6, 10, 2, 0, 0, 0)


def test_full_house_order():
    hand = [
        Card(9, Suit.SPADES),
        Card(9, Suit.DIAMONDS),
        Card(9, Suit.HEARTS),
        Card(14, Suit.CLUBS),
        Card(14, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (6, 9, 14, 0, 0, 0)


def test_quads():
    hand = [
        Card(8, Suit.SPADES),
        Card(8, Suit.DIAMONDS),
        Card(8, Suit.HEARTS),
        Card(8, Suit.CLUBS),
        Card(14, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (7, 8, 14, 0, 0, 0)


def test_quads_kicker():
    hand = [
        Card(5, Suit.SPADES),
        Card(5, Suit.DIAMONDS),
        Card(5, Suit.HEARTS),
        Card(5, Suit.CLUBS),
        Card(2, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (7, 5, 2, 0, 0, 0)


def test_straight_flush():
    hand = [
        Card(9, Suit.SPADES),
        Card(8, Suit.SPADES),
        Card(7, Suit.SPADES),
        Card(6, Suit.SPADES),
        Card(5, Suit.SPADES),
    ]
    assert Evaluator.mapper(hand) == (8, 9, 0, 0, 0, 0)


def test_straight_flush_wheel():
    hand = [
        Card(14, Suit.HEARTS),
        Card(2, Suit.HEARTS),
        Card(3, Suit.HEARTS),
        Card(4, Suit.HEARTS),
        Card(5, Suit.HEARTS),
    ]
    assert Evaluator.mapper(hand) == (8, 5, 0, 0, 0, 0)

def test_pair_kicker_ordering():
    hand1 = [Card(10,0), Card(10,1), Card(14,2), Card(9,3), Card(2,0)]
    hand2 = [Card(10,0), Card(10,1), Card(13,2), Card(9,3), Card(2,0)]

    assert Evaluator.mapper(hand1) > Evaluator.mapper(hand2)

def test_wheel_straight_low_ace():
    hand = [Card(14,0), Card(2,1), Card(3,2), Card(4,3), Card(5,0)]
    assert Evaluator.mapper(hand)[1] == 5

