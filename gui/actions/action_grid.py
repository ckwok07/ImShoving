from PyQt6.QtWidgets import QWidget, QGridLayout

from controller.action import Action
from .action_button import ActionButton
from PyQt6.QtCore import pyqtSignal

class ActionGrid(QWidget):
    action_clicked = pyqtSignal(Action)
    def __init__(self,) -> None:
        super().__init__()

        layout = QGridLayout(self)
        layout.setSpacing(12)

        actions = [Action(name = "FOLD", player = "hero"),
                   Action(name = "CHECK",player = "hero"), 
                   Action(name = "CALL", player = "hero"), 
                   Action(name = "RAISE", player = "hero", size = 2), 
                   Action(name= "ALL IN", player = "hero")]

        for i, action in enumerate(actions):
            button = ActionButton(action)
            button.clicked.connect(lambda x, a = action:self.action_clicked.emit(a))
            layout.addWidget(button, i // 3, i % 3)