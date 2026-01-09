from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

from main.model.Card import Card

class Board(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cards: list[QLabel] = []

        for i in range(5):
            label = QLabel("")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""QLabel { background-color: #2b2b2b;
                                color: white;
                                font-size: 22px;
                                border-radius: 6px;
                                padding: 10px;
                                min-width: 40px;
                                min-height: 70px; }""")
            self.cards.append(label)
            self.mainLayout.addWidget(label)

    def set_board(self, cards: list[Card]) -> None:
        for cardLabel in self.cards:
            cardLabel.setText("")

        for cardLabel, cardValue in zip(self.cards, cards):
            cardLabel.setText(str(cardValue))