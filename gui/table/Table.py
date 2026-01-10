from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from .Board import Board
from gui.actions.action_grid import ActionGrid
from .pot import PotLabel
from .ActionHistory import ActionHistory
from .HeroHand import HeroHand
from .HeroStack import HeroStack
from .VillainStack import VillainStack
from .VillainHand import VillainHand


class Table(QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.dealer = QLabel("D", self)
        self.dealer.setStyleSheet("background: black; color: white;")
        self.dealer.resize(24, 24)

        layout = QVBoxLayout(self)

        title = QLabel("table")
        title.setStyleSheet("color: white; font-size: 24px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background: #191919;")

        self.board = Board()
        self.pot_label = PotLabel()
        self.action_history = ActionHistory()
        self.hero_hand = HeroHand()
        self.hero_stack = HeroStack()
        self.villain_stack = VillainStack()
        self.villain_hand = VillainHand()

        self.pot_label.set_pot(controller.state.pot)
        self.controller.state_change = self.on_state_change
        self.on_state_change(self.controller.state)

        self.actions = ActionGrid()
        self.actions.action_clicked.connect(self.on_action)

        layout.addWidget(title)
        layout.addWidget(self.action_history, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.villain_hand, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.villain_stack, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.pot_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hero_hand, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hero_stack, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.actions, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
    
    def on_action(self, action) -> None:
        if self.controller.state.hand_over:
            return
        self.controller.handle_action(action)

    def on_state_change(self, state) -> None:
        self.pot_label.set_pot(state.pot)
        self.board.set_board(state.board)
        self.hero_hand.set_hand(state.hero_hand)
        self.hero_stack.set_hero_stack(state.hero_stack)
        self.villain_stack.set_villain_stack(state.villain_stack)
        self.villain_hand.set_hand(state.villain_hand)

        if state.button_index == 0:
            self.hero_button_pos()
        else:
            self.villain_button_pos()

        self.hero_hand.set_active(state.to_act_index == 0)
        self.villain_hand.set_active(state.to_act_index == 1)

        recent_actions = state.actions[-5:]
        self.action_history.set_actions(recent_actions)

    def hero_button_pos(self) -> None: 
        position = self.hero_hand.mapTo(self, self.hero_hand.rect().topLeft())
        self.dealer.move(position)

    def villain_button_pos(self) -> None: 
        position = self.villain_hand.mapTo(self, self.villain_hand.rect().topLeft())
        self.dealer.move(position)

