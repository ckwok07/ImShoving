from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class HeroStack(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""color: white;
                           font-size: 18px;
                           padding: 8px;""")
    
    def set_hero_stack(self, stack: float) -> None:
        self.setText(f"Stack: {stack:.2f}")

