from PyQt6.QtWidgets import QPushButton

class ResetStacks(QPushButton):
    def __init__(self) -> None:
        super().__init__("RESET STACKS")

        self.setStyleSheet("""
                           QPushButton {
                                background: #1b1b1b; 
                                font-size: 14px; 
                                font-weight: 600;
                                color: #7e7e7e;
                                border-radius: 6px;
                                padding: 6px 20px;
                           }
                           QPushButton:enabled:hover {
                                background-color: #3a3a3a
                           }
                           QPushButton:enabled:pressed {
                                background-color: #1f1f1f
                           }
                           
                           QPushButton:enabled {
                                background-color: #2b2b2b;
                                color: white;
                            }""")
                                    
