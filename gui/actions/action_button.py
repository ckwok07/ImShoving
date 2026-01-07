from PyQt6.QtWidgets import QPushButton

from controller.action import Action

class ActionButton(QPushButton):
    def __init__(self, action: Action) -> None:
        self.action = action
        super().__init__(self._label(action))

        self.setStyleSheet("""
                           QPushButton {
                                background: 2b2b2b; 
                                font-size: 14px; 
                                color: white;
                           }
                           QPushButton:hover {
                                background-color: #3a3a3a
                           }
                           QPushButton:pressed {
                                background-color: #1f1f1f
                           }""")
    
    def _label(self, action: Action) -> str:
        if action.size is None:
            return action.name
        return f"{action.name} {action.size}"