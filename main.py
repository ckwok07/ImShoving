from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel
import sys

from gui.table.Table import Table

def main() -> None:
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("ImAllIn")
    window.resize(1200,800)

    central = QWidget()
    layout = QHBoxLayout(central)

    left_panel = QLabel("left_panel")
    left_panel.setStyleSheet("background: #191919; color: white;")
    right_panel = QLabel("right_panel")
    right_panel.setStyleSheet("background: #191919; color: white;")

    table = Table()

    layout.addWidget(left_panel)
    layout.addWidget(table, 1)
    layout.addWidget(right_panel)

    window.setCentralWidget(central)
    window.show()

    app.exec()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()