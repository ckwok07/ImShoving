from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from .Board import Board

class Table(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("table")
        title.setStyleSheet("color: white; font-size: 24px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background: #191919;")

        self.board = Board()

        layout.addWidget(title)
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

        self.board.set_board(["1", "2", "3"])

        

