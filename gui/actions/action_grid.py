from PyQt6.QtWidgets import QWidget, QGridLayout

from controller.action import Action
from .action_button import ActionButton
from PyQt6.QtCore import pyqtSignal

class ActionGrid(QWidget):
    action_clicked = pyqtSignal(Action)
    def __init__(self,) -> None:
        super().__init__()

        self.layout = QGridLayout(self)
        self.layout.setSpacing(12)
        self.setMinimumHeight(90) 

        # actions = [Action(name = "FOLD", player = "hero"),
        #            Action(name = "CHECK",player = "hero"), 
        #            Action(name = "CALL", player = "hero"), 
        #            Action(name = "RAISE", player = "hero", size = 2), 
        #            Action(name= "ALL IN", player = "hero")]
    
    def set_actionGrid(self, actions: list[Action]) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        for i, action in enumerate(actions):
            button = ActionButton(action)
            button.clicked.connect(lambda x, a = action:self.action_clicked.emit(a))
            self.layout.addWidget(button, i // 3, i % 3)