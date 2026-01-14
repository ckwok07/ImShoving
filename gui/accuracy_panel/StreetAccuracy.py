from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QTimer

from controller.decisionAccuracy import DecisionQuality

class StreetAccuracy(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QHBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("QWidget {background: red;}")


        self.preflop = QLabel("PreFlop: --")
        self.flop = QLabel("Flop: --")
        self.turn = QLabel("Turn: --")
        self.river = QLabel("River: --")

        for label in (self.preflop, self.flop, self.turn, self.river):
            layout.addWidget(label)
            label.setStyleSheet("background: transparent; color: white; font-weight: bold;")

        self.labels = {
            "PREFLOP": self.preflop,
            "FLOP": self.flop,
            "TURN": self.turn,
            "RIVER": self.river,
        }

        layout.addStretch()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-weight: bold; font-size: 13px;")

    def update_stats(self, decisions: list[DecisionQuality]) -> None:
        buckets = {"PREFLOP": [], "FLOP": [], "TURN":[], "RIVER":[]}

        for decision in decisions:
            if decision.street in buckets:
                buckets[decision.street].append(decision.accuracy)

        for street, accuracy in buckets.items():
            if accuracy:
                avg = sum(accuracy) / len(accuracy)
                text = f"{street.title()[:4]}: {avg:.0f}%"
            else:
                text = f"{street.title()[:4]}: --"

            self.labels[street].setText(text)
