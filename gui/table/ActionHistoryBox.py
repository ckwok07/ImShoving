from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

class ActionHistoryBox(QWidget):
    def __init__(self, left_text: str, action_text: str):
        super().__init__()

        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(3, 2, 3, 2)
        outer_layout.setSpacing(0)

        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(6, 2, 6, 2)
        left_layout.setSpacing(2)

        left_label = QLabel(left_text)
        left_label.setStyleSheet("QLabel {color: #6e6e6e; font-weight: 550;}")
        left_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        action_label = QLabel(action_text)
        action_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        action_label.setStyleSheet(""" QLabel {
                                   background: #3a3a3a; 
                                   color: white; 
                                   border-radius: 
                                   6px; padding: 4px 6px; 
                                   font-weight: bold; }""")

        left_layout.addWidget(left_label)
        left_layout.addWidget(action_label)

        outer_layout.addWidget(left_container)
        self.setStyleSheet("""QWidget {
                           background: #2b2b2b;
                           border-radius: 6px;
                           padding: 3px; }""")
