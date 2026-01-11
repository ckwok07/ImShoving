from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy
from .ActionHistoryBox import ActionHistoryBox

from controller.action import Action

class ActionHistory(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.items: list[QLabel] = []

        title = QLabel("actions")
        title.setStyleSheet("color: white;")
        self.layout.addWidget(title)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

    def add_action(self, action: Action) -> None:
        text = self.formatAction(action)

        chip = ActionHistoryBox(text)
        self.layout.addWidget(chip)
        self.items.append(chip)
    
    def add_actions(self, actions: list[Action]) -> None:
        for action in actions:
            self.add_action(action)
    
    def clear_actions(self) -> None:
        for item in self.items:
            self.layout.removeWidget(item)
            item.deleteLater()
        self.items.clear()

    def set_actions(self, actions: list[Action]) -> None:
            self.clear_actions()
            self.add_actions(actions)

            scroll = self.parent()
            if scroll:
                scroll = self.parentWidget()
                while scroll and not hasattr(scroll, "horizontalScrollBar"):
                    scroll = scroll.parentWidget()

                if scroll:
                    bar = scroll.horizontalScrollBar()
                    bar.setValue(bar.maximum())

                bar.setValue(bar.maximum())
    
    def formatAction(self, action) -> str:
        if action.size is None:
            return f"{action.player}:{action.name}"
        return f"{action.player} {action.name} {action.size}"