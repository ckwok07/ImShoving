from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout

class MoveListChip(QWidget):
    def __init__(self, quality: str = "", accuracy: float = 0.0, equity: float  = 0.0):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)
        layout.setSpacing(6)

        self.quality_label = QLabel()
        self.accuracy_label = QLabel()
        self.equity_label = QLabel()

        layout.addWidget(self.quality_label)
        layout.addWidget(self.accuracy_label)
        layout.addWidget(self.equity_label)

        self.setStyleSheet("""
            QWidget {
                background: #2b2b2b;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 11px;
            }
        """)

        self.set_data(quality, accuracy, equity)

    def set_data(self, quality: str, accuracy: float, equity: float):
        self.quality_label.setText(quality)
        self.accuracy_label.setText(f"ACCURACY: {accuracy:.1f}%")
        self.equity_label.setText(f"EQUITY: {equity * 100:.1f}%")
