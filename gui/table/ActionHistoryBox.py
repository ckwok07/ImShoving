from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from controller.action import Action


class ActionHistoryBox(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setStyleSheet("""QLabel {background: #2b2b2b; 
                           color: #eaeaea; }""")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
