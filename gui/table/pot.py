from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, pyqtProperty, QPropertyAnimation

class PotLabel(QLabel):
    def __init__(self) -> None:
        super().__init__("Pot: 0.0")

        self.pot_value = 0.0

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""QLabel { background-color: #2b2b2b;
                           color: white;
                           font-size: 18px;
                           font-weight: bold;
                           padding: 8px;
                           border-radius: 6px;
                           border: 1.5px solid #8b5cf6 }""")

        self._anim = QPropertyAnimation(self, b"potValue")
        self._anim.setDuration(1000)

        self.update_text()
    
    def get_pot_value(self):
        return self.pot_value

    def set_pot_value(self, value):
        self.pot_value = value
        self.update_text()

    potValue = pyqtProperty(float, fget=get_pot_value, fset=set_pot_value)

    def set_pot(self, pot: float) -> None:
        if self.pot_value == 0.0:
            self.pot_value = pot
            self.update_text()
            return
        
        self._anim.stop()
        self._anim.setStartValue(self.pot_value)
        self._anim.setEndValue(pot)
        self._anim.start()

    def update_text(self):
        self.setText(f"{self.pot_value:.1f} BB")