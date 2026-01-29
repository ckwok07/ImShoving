from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel
import sys

from controller.appController import AppController
from controller.gameState import GameState
from gui.table.Table import Table
from gui.accuracy_panel.Panel import Panel
from gui.right_panel.RPanel import RPanel

def main() -> None:
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("ImAllIn")
    window.resize(1200,800)
    # window.setFixedHeight(900)
    # window.setFixedWidth(1500)
    window.setStyleSheet("""background-color: #121212;
                         border-radius: 6px;""")


    central = QWidget()
    layout = QHBoxLayout(central)

    state = GameState(street = "PREFLOP", 
                      board = [], 
                      pot = 0,
                      current_bet = 0,
                      hero_amt = 0,
                      villain_amt = 0,
                      hero_stack = 100,
                      villain_stack = 100,
                      hero_all_in = False,
                      villain_all_in = False,)
    controller = AppController(state)
    table = Table(controller)
    panel = Panel(controller)
    rpanel = RPanel(controller)

    def on_state_change(state):
        table.on_state_change(state)
        panel.on_state_change(state)

    controller.state_change = on_state_change

    layout.addWidget(panel)
    layout.addWidget(table, 1)
    layout.addWidget(rpanel)

    window.setCentralWidget(central)
    window.show()

    sys.exit(app.exec())

    

if __name__ == "__main__":
    main()