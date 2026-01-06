from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class Board(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cards = []

        for i in range(5):
            card = QLabel("card")
            card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card.setStyleSheet("background: #2a2a2a; color: white; font-size: 18px;")
            self.cards.append(card)
            layout.addWidget(card)

    def set_board(self, cards: list[str]) -> None:
        for cardLabel, cardValue in zip(self.cards, cards):
            cardLabel.setText(cardValue)