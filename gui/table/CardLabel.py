from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from main.model.Card import Card
from main.model.Rank import Rank
from main.model.Suit import Suit

class CardLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""QLabel {background-color: #2b2b2b;
                           border-radius: 6px;}""")
        
        self.setFixedSize(65, 100)
        
        self.card = None
        self.face_up = True
        
    def set_card(self, card: Card):
        self.card = card
        self.face_up = True
        self.update()

    def hide_card(self):
        self.face_up = False
        self.setPixmap(QPixmap())

    def clear(self):
        self.card = None
        self.setPixmap(QPixmap())

    def update(self):
        if not self.card:
            self.clear()
            return
        
        filename = f"assets/cards/image.png"
        pixmap = QPixmap(filename)
        scaled = pixmap.scaled(self.size(), 
                               Qt.AspectRatioMode.KeepAspectRatio, 
                               Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(scaled)

