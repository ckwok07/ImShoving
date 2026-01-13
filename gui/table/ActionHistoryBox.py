from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from controller.action import Action


class ActionHistoryBox(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(50)
        self.setStyleSheet("""QLabel {background: #2b2b2b; 
                           color: white;
                           border-radius: 4px;
                           padding: 6px; }""")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
