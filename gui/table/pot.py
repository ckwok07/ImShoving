from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class PotLabel(QLabel):
    def __init__(self) -> None:
        super().__init__("Pot: 0.0")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            color: white;
            font-size: 18px;
            padding: 8px;
        """)

    def set_pot(self, pot: float) -> None:
        self.setText(f"Pot: {pot:.2f}")
