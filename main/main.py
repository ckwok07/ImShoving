from model.Deck import Deck


def main() -> None:
    deck = Deck()
    deck.shuffle()

    c1 = deck.draw()
    c2 = deck.draw()

    print(c1.rank.display() + c1.suit.display())
    print(c2.rank.display() + c2.suit.display())

if __name__ == "__main__":
    main()