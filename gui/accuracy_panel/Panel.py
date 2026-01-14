from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt, QTimer

from controller.gameState import GameState
from .AccuracyDash import AccuracyDash
from .DecisionList import DecisionList

class Panel(QWidget):

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""QWidget {background: #191919;}""")
    
        title = QLabel("ACCURACY")
        title.setStyleSheet("""QLabel {background-color: #191919;
                             color: white;
                             font-size: 24px;
                             font-weight: 600;
                             padding: 8px}""")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        
        self.dash = AccuracyDash()
        self.decisions = DecisionList()

        layout.addWidget(self.dash)
        layout.addWidget(self.decisions)

    def on_state_change(self, state: GameState):
        self.dash.update(state, self.controller.decision_quality)