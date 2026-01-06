from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class Table(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("table")
        title.setStyleSheet("color: white; font-size: 24px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background: #191919;")

        layout.addWidget(title)

