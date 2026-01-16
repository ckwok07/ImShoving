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
        
        self.setFixedSize(75, 105)
        
        self.card = None
        self.face_up = True
        
    def set_card(self, card: Card, face_up = True):
        self.card = card
        self.face_up = face_up
        self.refresh()

    def hide_card(self):
        self.face_up = False
        self.refresh()

    def show_card(self):
        self.face_up = True
        self.refresh()

    def clear(self):
        self.card = None
        self.setPixmap(QPixmap())


    def refresh(self):
        if not self.card:
            self.clear()
            return

        if self.face_up:
            filename = f"assets/cards/{self.card}.png"
        else:
            filename = "assets/cards/back.png"

        pixmap = QPixmap(filename)

        dpr = self.devicePixelRatioF()

        target_size = self.size() * dpr

        scaled = pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        scaled.setDevicePixelRatio(dpr)
        self.setPixmap(scaled)
