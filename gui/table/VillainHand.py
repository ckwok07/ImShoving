from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from main.model.Card import Card
from .CardLabel import CardLabel

class VillainHand(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cards = []

        for i in range(2):
            cardLabel = CardLabel()
            self.cards.append(cardLabel)
            self.mainLayout.addWidget(cardLabel)
        
    def set_hand(self, cards: list[Card] | None) -> None:
        for cardLabel in self.cards:
            cardLabel.clear()

        if not cards:
            return

        for cardLabel, card in zip(self.cards, cards):
            cardLabel.set_card(card)

    def set_active(self, active: bool):
        if active:
            self.setStyleSheet("QWidget { border: 3px solid orange; border-radius: 8px; } ")
        else:
            self.setStyleSheet("QWidget { border: 3px solid transparent; border-radius: 8px; }")
