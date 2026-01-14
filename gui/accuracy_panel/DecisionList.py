from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout

class DecisionList(QWidget):
    def __init__(self) -> None:
        super().__init__()

        scroll = QScrollArea()
        dlist = QWidget()
        self.layout = QVBoxLayout(dlist)

        scroll.setWidget(dlist)

        main = QVBoxLayout(self)
        main.addWidget(scroll)