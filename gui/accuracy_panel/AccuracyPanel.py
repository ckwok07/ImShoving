from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from .AccuracyDash import AccuracyDash
from .DecisionList import DecisionList

class AcuraccyPanel(QWidget):

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout(self)

        title = QLabel("Accuracy")
        title.setStyleSheet("color: white; font-size: 24px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dash = AccuracyDash()
        self.decisions = DecisionList()

        layout.addWidget(self.dash)
        layout.addWidget(self.decisions)