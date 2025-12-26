import pytest
from main.model.Range import Range
from main.model.Card import Card
from main.model.Suit import Suit
from main.model.Rank import Rank

def test_all_hands_count():
    r = Range()
    assert Range.ALL_HANDS is not None
    assert len(Range.ALL_HANDS) == 1326

def test_all_hands_structure():
    r = Range()

    for hand in Range.ALL_HANDS:
        assert len(hand) == 2
        c1, c2 = hand
        assert not (c1.rank == c2.rank and c1.suit == c2.suit)

def test_is_blocked_true():
    r = Range()
    known = [Card(14, Suit.SPADES)]
    hand = [Card(14, Suit.SPADES), Card(13, Suit.HEARTS)]

    assert r.is_blocked(hand, known) is True

def test_is_blocked_false():
    r = Range()
    known = [Card(Rank.ACE, Suit.SPADES)]
    hand = [Card(Rank.ACE, Suit.HEARTS), Card(Rank.KING, Suit.HEARTS)]

    assert r.is_blocked(hand, known) is False

def test_available_hands_blocks_known_cards():
    r = Range()

    known = [Card(Rank.ACE, Suit.SPADES)]
    avail = r.available_hands(known)

    for hand in avail:
        for card in hand:
            assert not (card.rank == Rank.ACE and card.suit == Suit.SPADES)

def test_available_hands_sizes():
    r = Range()

    known1 = []
    known2 = [Card(Rank.ACE, Suit.SPADES)]

    avail1 = r.available_hands(known1)
    avail2 = r.available_hands(known2)

    assert len(avail2) < len(avail1)

def test_sample_hand_blocked():
    r = Range()
    known = [
        Card(14, Suit.SPADES),
        Card(13, Suit.HEARTS),
    ]

    avail = r.available_hands(known)

    for hand in avail:
        for card in hand:
            assert not (
                (card.rank == 14 and card.suit == Suit.SPADES.value) or
                (card.rank == 13 and card.suit == Suit.HEARTS.value)
            )
