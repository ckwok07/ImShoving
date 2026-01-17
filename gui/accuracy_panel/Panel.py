from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt, QTimer

from controller.gameState import GameState
from gui.accuracy_panel.MoveList import MoveList
from .AccuracyDash import AccuracyDash

class Panel(QWidget):

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.controller.accuracy_panel = self
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""QWidget {background: #191919;}""")
    
        title = QLabel("ACCURACY")
        title.setStyleSheet("""QLabel {background-color: #191919;
                             color: #bbbbbb;
                             font-size: 24px;
                             font-weight: 600;
                             padding: 8px}""")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        
        self.dash = AccuracyDash()
        layout.addWidget(self.dash)

        title2 = QLabel("DECISION ANALYSIS")
        title2.setStyleSheet("""QLabel {background-color: #191919;
                             color: #bbbbbb;
                             font-size: 24px;
                             font-weight: 600;
                             padding: 4px}""")
        title2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title2)

        self.move_list = MoveList()

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.move_list)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(self.scroll)



    def on_state_change(self, state: GameState):
        self.dash.update(state, self.controller.decision_quality)

    def on_decision_made(self):
        self.move_list.set_decisions(self.controller.decision_quality)
