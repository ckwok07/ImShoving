from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from .Board import Board
from gui.actions.action_grid import ActionGrid

class Table(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("table")
        title.setStyleSheet("color: white; font-size: 24px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background: #191919;")

        self.board = Board()
        self.actions = ActionGrid()

        layout.addWidget(title)
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.actions, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

        self.board.set_board(["1", "2", "3"])

        

