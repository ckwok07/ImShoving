from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtProperty, QPropertyAnimation


class HeroStack(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.stack_value = 0.0

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""QLabel { background: #2b2b2b;
                           color: white;
                           font-size: 16px;
                           font-weight: bold;
                           padding: 8px;
                           border-radius: 35px;
                           border: 3px solid #8B5CF6 }""")
        self.setFixedSize(70, 70)

        self._anim = QPropertyAnimation(self, b"stackValue")
        self._anim.setDuration(500)
        
        self.update_text()
    
    def get_stack_value(self):
        return self.stack_value
    
    def set_stack_value(self, value):
        self.stack_value = value
        self.update_text()

    stackValue = pyqtProperty(float, fget=get_stack_value, fset=set_stack_value)
    
    def set_hero_stack(self, stack: float) -> None:
        if self.stack_value == 0.0:
            self.stack_value = stack
            self.update_text()
            return
        
        self._anim.stop()
        self._anim.setStartValue(self.stack_value)
        self._anim.setEndValue(stack)

        self.stack_value = stack

        self._anim.start()


    def update_text(self):
        self.setText(f"<div style='line-height:1.1; text-align:center;'>BB<br>{self.stack_value:.1f}</div>")
        self.setTextFormat(Qt.TextFormat.RichText)


