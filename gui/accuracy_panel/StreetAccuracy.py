from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QTimer

from controller.decisionAccuracy import DecisionQuality

class StreetAccuracy(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QHBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("QWidget {background: #2b2b2b;}")

        self.labels = {}
        
        for street in ["PREFLOP", "FLOP", "TURN", "RIVER"]:
            col = self.create_street_column(street)
            layout.addLayout(col, 1)
    
    def create_street_column(self, street: str) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(2)

        title = QLabel(street.upper())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #bbbbbb; font-size: 12px; font-weight: 700;")

        value = QLabel("--")
        value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")

        layout.addWidget(title)
        layout.addWidget(value)

        self.labels[street] = value
        return layout

    def update_stats(self, decisions: list[DecisionQuality]) -> None:
        buckets = {"PREFLOP": [], "FLOP": [], "TURN":[], "RIVER":[]}

        for decision in decisions:
            if decision.street in buckets:
                buckets[decision.street].append(decision.accuracy)

        for street, accuracy in buckets.items():
            if accuracy:
                avg = sum(accuracy) / len(accuracy)
                text = f"{avg:.0f}%"
            else:
                text = "--"

            self.labels[street].setText(text)
