from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy

from controller.decisionAccuracy import DecisionQuality
from controller.gameState import GameState
from .StreetAccuracy import StreetAccuracy
from .AccuracyGraph import AccuracyGraph

class AccuracyDash(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("QWidget {background: #191919;}")

        self.street_accuracy = StreetAccuracy()
        layout.addWidget(self.street_accuracy)

        self.graph = AccuracyGraph()
        layout.addWidget(self.graph)

    def update(self, state: GameState, decision_quality_list: list[DecisionQuality]):
        self.street_accuracy.update_stats(decision_quality_list)

        values = []
        total = 0.0
        for i, d in enumerate(decision_quality_list, 1):
            total += d.accuracy
            values.append(total / i)
        self.graph.set_data(values)
