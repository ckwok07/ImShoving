from PyQt6.QtWidgets import QPushButton

class ActionButton(QPushButton):
    def __init__(self, label: str) -> None:
        super().__init__(label)

        self.setStyleSheet("background: #2b2b2b; font-size: 14px")