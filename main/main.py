from model.Deck import Deck


def main() -> None:
    deck = Deck()
    deck.shuffle()

    hand = deck.deal(2)
    board = deck.deal(5)
    villian = deck.deal(2)

    print("hand:")
    for card in hand:
        print(card.rank.display() + card.suit.display())

    print("board:")

    for card in board:
        print(card.rank.display() + card.suit.display())

if __name__ == "__main__":
    main()