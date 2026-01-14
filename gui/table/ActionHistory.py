from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from .ActionHistoryBox import ActionHistoryBox
from controller.action import Action


class ActionHistory(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.items: list[QLabel] = []
        self.setFixedHeight(65)

        title = QLabel("ACTIONS")
        title.setStyleSheet("""QLabel {color: white; 
                            font-weight: bold;
                            padding: 8px; }""")
        self.layout.addWidget(title)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

    def add_action(self, action: Action) -> None:
        left_text, action_text = self.formatAction(action)
        chip = ActionHistoryBox(left_text, action_text)

        chip.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        chip.setMinimumWidth(chip.sizeHint().width())

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
        self.adjustSize()
        self.updateGeometry()

        scroll = self.parentWidget()
        while scroll and not hasattr(scroll, "horizontalScrollBar"):
            scroll = scroll.parentWidget()

        if scroll:
            bar = scroll.horizontalScrollBar()
            bar.setValue(bar.maximum())

    def formatAction(self, action: Action):
        if action.name == "Post Blind":
            action_name = "BLIND"
        else:
            action_name = action.name.upper()

        if action.player == "villain":
            player = "VILLAIN"
        else:
            player = "HERO"

        left_text = f"{player}  {action.pot_after}"

        return left_text, action_name
