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
        
        self.previous_board_size = 0

    def set_board(self, cards: list[Card]) -> None:
        if not cards:
            for cardLabel in self.cards:
                cardLabel.clear()
            self.previous_board_size = 0
            return

        current_size = len(cards)
        
        for i in range(self.previous_board_size, current_size):
            delay = (i - self.previous_board_size) * 500
            self.cards[i].set_card(cards[i], face_up=True, animate=True, delay=delay)
        
        for i in range(current_size, 5):
            self.cards[i].clear()
        
        self.previous_board_size = current_size