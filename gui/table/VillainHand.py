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
        
        self.current_cards = None
        
    def set_hand(self, cards: list[Card] | None, reveal = False) -> None:
        if not cards:
            for cardLabel in self.cards:
                cardLabel.clear()
            self.current_cards = None
            return

        cards_changed = (self.current_cards is None or 
                        len(cards) != len(self.current_cards) or
                        any(c1 != c2 for c1, c2 in zip(cards, self.current_cards)))
        
        should_animate = cards_changed
        
        for i, (cardLabel, card) in enumerate(zip(self.cards, cards)):
            delay = i * 1000 if should_animate else 0
            cardLabel.set_card(card, face_up=reveal, animate=should_animate, delay=delay)
        
        self.current_cards = cards.copy() if cards else None

    def set_active(self, active: bool):
        if active:
            self.setStyleSheet("QWidget { border: 3px solid orange; border-radius: 8px; } ")
        else:
            self.setStyleSheet("QWidget { border: 3px solid transparent; border-radius: 8px; }")

    def reveal(self):
        for cardLabel in self.cards:
            cardLabel.show_card()