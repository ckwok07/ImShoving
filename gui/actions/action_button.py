from PyQt6.QtWidgets import QPushButton

class ActionButton(QPushButton):
    def __init__(self, label: str) -> None:
        super().__init__(label)

        self.setStyleSheet("""
                           QPushButton {
                                background: 2b2b2b; 
                                font-size: 14px; 
                                color: white;
                           }
                           QPushButton:hover {
                                background-color: #3a3a3a
                           }""")