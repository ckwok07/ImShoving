from PyQt6.QtWidgets import QPushButton

class NextHand(QPushButton):
    def __init__(self) -> None:
        super().__init__("NEXT HAND")

        self.setStyleSheet("""
                           QPushButton {
                                background: #2b2b2b; 
                                font-size: 14px; 
                                font-weight: 600;
                                color: white;
                                border-radius: 6px;
                                padding: 6px 20px;
                           }
                           QPushButton:hover {
                                background-color: #3a3a3a
                           }
                           QPushButton:pressed {
                                background-color: #1f1f1f
                           }""")
        
