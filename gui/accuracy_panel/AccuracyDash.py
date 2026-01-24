from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy

from controller.decisionAccuracy import DecisionQuality
from controller.gameState import GameState
from .StreetAccuracy import StreetAccuracy
from .AccuracyGraph import AccuracyGraph
from .AccuracyGraph import LegendWidget

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

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)

        # Add legend
        legend = LegendWidget(
            labels=["Average", "Raw", "5 Turn"],
            colors=["#ffa500", "#7ce7e1", "#d6d6d6"]
        )
        container_layout.addWidget(legend)

        self.graph = AccuracyGraph()
        container_layout.addWidget(self.graph)

        layout.addWidget(container)

    def update(self, state: GameState, decision_quality_list: list[DecisionQuality]):
        self.street_accuracy.update_stats(decision_quality_list)

        avg_accuracy = []
        raw_accuracy = []
        rolling5_accuracy = []
        
        total = 0.0
        for i, d in enumerate(decision_quality_list, 1):
            total += d.accuracy
            avg_accuracy.append(total / i)
            raw_accuracy.append(d.accuracy)

            start = max(0, len(raw_accuracy) - 5)
            rolling5_list = raw_accuracy[start:]
            rolling5_accuracy.append(sum(rolling5_list) / len(rolling5_list))
        self.graph.set_data([avg_accuracy, raw_accuracy, rolling5_accuracy])
