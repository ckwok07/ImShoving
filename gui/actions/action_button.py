from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from controller.action import Action

class ActionButton(QPushButton):
    def __init__(self, action: Action) -> None:
        self.action = action
        super().__init__(self._label(action))

        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setMouseTracking(True)

        self.setStyleSheet("""
                           QPushButton {
                                background: #2b2b2b; 
                                font-size: 14px; 
                                font-weight: 500;
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
    
    def _label(self, action: Action) -> str:
          if action.size == 0:
            return action.name
          elif action.name == "RAISE":
               return f"{action.name} TO {action.size}"
          return f"{action.name} {action.size}"