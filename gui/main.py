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
    left_panel.setStyleSheet("background: #191919; color: white;")
    center_panel = QLabel("center_panel")
    center_panel.setStyleSheet("background: #121212; color: white;")
    right_panel = QLabel("right_panel")
    right_panel.setStyleSheet("background: #191919; color: white;")

    layout.addWidget(left_panel)
    layout.addWidget(center_panel, 1)
    layout.addWidget(right_panel)

    window.setCentralWidget(central)
    window.show()

    app.exec()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()