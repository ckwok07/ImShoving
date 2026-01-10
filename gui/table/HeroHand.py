from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from main.model.Card import Card

class HeroHand(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cards: list[QLabel] = []

        for i in range(2):
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
        
    def set_hand(self, cards: list[Card] | None) -> None:
        for label in self.cards:
            label.setText("")

        if not cards:
            return

        for label, card in zip(self.cards, cards):
            label.setText(str(card))
    
    def set_active(self, active: bool):
        if active:
            self.setStyleSheet("QWidget {border: 3px solid orange; border-radius: 8px;} ")
        else:
            self.setStyleSheet("QWidget {border: 3px solid transparent; border-radius: 8px;}")

