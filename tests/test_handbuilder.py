
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