from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

from main.model.Card import Card
from .CardLabel import CardLabel

class Board(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cards = []

        for i in range(5):
            cardLabel = CardLabel()
            self.cards.append(cardLabel)
            self.mainLayout.addWidget(cardLabel)

    def set_board(self, cards: list[Card]) -> None:
        for cardLabel in self.cards:
            cardLabel.clear()

        if not cards:
            return

        for cardLabel, card in zip(self.cards, cards):
            cardLabel.set_card(card)