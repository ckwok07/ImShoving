from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class PotLabel(QLabel):
    def __init__(self) -> None:
        super().__init__("Pot: 0.0")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""QLabel { background-color: #2b2b2b;
                           color: white;
                           font-size: 18px;
                           font-weight: bold;
                           padding: 8px;
                           border-radius: 6px;
                           border: 1.5px solid #8b5cf6 }""")

    def set_pot(self, pot: float) -> None:
        self.setText(f"{pot:.1f} BB")
