from PyQt6.QtWidgets import QWidget, QGridLayout
from .action_button import ActionButton

class ActionGrid(QWidget):
    def __init__(self,) -> None:
        super().__init__()

        layout = QGridLayout(self)
        layout.setSpacing(12)

        actions = ["CHECK", "BET 1", "BET 2", "ALL IN"]

        for i, label in enumerate(actions):
            button = ActionButton(label)
            layout.addWidget(button, i // 3, i % 3)