from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt, QTimer

from controller.decisionAccuracy import DecisionQuality
from .MoveListChip import MoveListChip

class MoveList(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setMinimumHeight(0)
        self.layout.setContentsMargins(6, 4, 6, 4)
        self.layout.setSpacing(6)
        

    def set_decisions(self, decisions: list[DecisionQuality]):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for d in decisions:
            chip = MoveListChip(d.label, d.accuracy, d.equity_before)
            self.layout.insertWidget(0, chip)
