from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel
import sys

from controller.appController import AppController
from controller.gameState import GameState
from gui.table.Table import Table

def main() -> None:
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("ImAllIn")
    window.resize(1200,800)
    window.setStyleSheet("background-color: #121212;")


    central = QWidget()
    layout = QHBoxLayout(central)

    left_panel = QLabel("left_panel")
    left_panel.setStyleSheet("background: #191919; color: white;")
    right_panel = QLabel("right_panel")
    right_panel.setStyleSheet("background: #191919; color: white;")

    state = GameState(street="flop", board=["5s", "5d", "4h"], pot=16.5)
    controller = AppController(state)
    table = Table(controller)

    layout.addWidget(left_panel)
    layout.addWidget(table, 1)
    layout.addWidget(right_panel)

    window.setCentralWidget(central)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()