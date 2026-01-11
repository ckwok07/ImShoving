from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class VillainStack(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""QLabel { background: #2b2b2b;
                           color: white;
                           font-size: 16px;
                           font-weight: bold;
                           padding: 8px;
                           border-radius: 35px;
                           border: 3px solid #8B5CF6 }""")
        self.setFixedSize(70, 70)
    
    def set_villain_stack(self, stack: float) -> None:
        self.setText(f"<div style='line-height:1.1; text-align:center;'>BB<br>{stack:.1f}</div>")
        self.setTextFormat(Qt.TextFormat.RichText)

