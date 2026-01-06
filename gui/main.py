from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel
import sys

def main() -> None:
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("ImAllIn")
    window.resize(1200,800)

    central = QWidget()
    layout = QHBoxLayout(central)

    left_panel = QLabel("left_panel")
    center_panel = QLabel("center_panel")
    right_panel = QLabel("right_panel")

    layout.addWidget(left_panel)
    layout.addWidget(center_panel)
    layout.addWidget(right_panel)

    window.setCentralWidget(central)
    window.show()

    app.exec()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()