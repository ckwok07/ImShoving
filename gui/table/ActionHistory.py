from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from controller.action import Action

class ActionHistory(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.items: list[QLabel] = []

        title = QLabel("actions")
        title.setStyleSheet("color: white;")
        self.layout.addWidget(title)

    def add_action(self, action: Action) -> None:
        label = QLabel(self.formatAction(action))
        self.layout.addWidget(label)
        self.items.append(label)
    
    def add_actions(self, actions: list[Action]) -> None:
        for action in actions:
            self.add_action(action)
    
    def clear_actions(self) -> None:
        for item in self.items:
            self.layout.removeWidget(item)
            item.deleteLater()
        self.items.clear()
    
    def formatAction(self, action) -> str:
        if action.size is None:
            return action.name
        return f"{action.name} {action.size}"