from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AccuracyGraph(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Accuracy Graph"))

        self.setStyleSheet("QWidget {background: #191919;}")