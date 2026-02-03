from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt, QTimer

from controller.gameState import GameState
from .Board import Board
from gui.actions.action_grid import ActionGrid
from .pot import PotLabel
from .ActionHistory import ActionHistory
from .HeroHand import HeroHand
from .HeroStack import HeroStack
from .VillainStack import VillainStack
from .VillainHand import VillainHand
from .NextHand import NextHand
from .ResetStacks import ResetStacks


class Table(QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setStyleSheet("background: #191919;")

        self.board = Board()
        self.pot_label = PotLabel()
        self.action_history = ActionHistory()

        self.action_scroll = QScrollArea()
        self.action_scroll.viewport().installEventFilter(self)
        self.action_scroll.setWidget(self.action_history)
        self.action_scroll.setWidgetResizable(True)
        self.action_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self.action_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.action_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.action_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.action_scroll.setFixedHeight(45)


        self.hero_hand = HeroHand()
        self.hero_stack = HeroStack()
        self.villain_stack = VillainStack()
        self.villain_hand = VillainHand()
        self.dealer = QLabel("D", self.hero_hand)
        self.dealer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dealer.setStyleSheet("""QLabel {background: #191919;
                                   color: white;
                                   border-radius: 15px;
                                   border: none;
                                   font-size: 14px;
                                   font-weight: bold;}""")
        self.dealer.setFixedSize(30, 30)
        self.dealer.raise_()

        self.pot_label.set_pot(controller.state.pot)
        #self.controller.state_change = self.on_state_change
        #self.on_state_change(self.controller.state)
        QTimer.singleShot(0, self.init_positions)

        self.actions = ActionGrid()
        self.actions.action_clicked.connect(self.on_action)
        self.next_hand = NextHand()
        self.reset_stacks = ResetStacks()
        self.next_hand.clicked.connect(self.on_next_hand_clicked)
        self.reset_stacks.clicked.connect(self.on_reset_stacks_clicked)

        layout.addWidget(self.action_scroll)

        villain_row = QWidget()
        villain_row.setStyleSheet("background: transparent;")

        villain_layout = QHBoxLayout(villain_row)
        villain_layout.setContentsMargins(0, 0, 0, 0)
        villain_layout.setSpacing(10)

        villain_layout.addWidget(self.villain_stack)
        villain_layout.addWidget(self.villain_hand)

        layout.addWidget(villain_row, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.pot_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignHCenter)

        hero_row = QWidget()
        hero_row.setStyleSheet("background: transparent;")
        hero_layout = QHBoxLayout(hero_row)
        hero_layout.setContentsMargins(0, 0, 0, 0)
        hero_layout.setSpacing(10)

        hero_layout.addWidget(self.hero_stack)
        hero_layout.addWidget(self.hero_hand)

        layout.addWidget(hero_row, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.actions, alignment=Qt.AlignmentFlag.AlignHCenter)
        hero_layout.setSpacing(20)
        layout.addWidget(self.next_hand, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(10)
        layout.addWidget(self.reset_stacks, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
    
    def on_action(self, action) -> None:
        if self.controller.state.hand_over:
            return
        self.controller.handle_action(action)
    
    def init_positions(self):
        self.on_state_change(self.controller.state)

    def on_state_change(self, state: GameState) -> None:
        if state.street == "PREFLOP" and len(state.board) == 0:
            self.board.previous_board_size = 0
        
        self.pot_label.set_pot(state.pot)
        self.hero_hand.set_hand(state.hero_hand)
        self.hero_stack.set_hero_stack(state.hero_stack)
        self.villain_stack.set_villain_stack(state.villain_stack)
        self.villain_hand.set_hand(state.villain_hand, state.show_villain_cards)

        actions = self.controller.get_hero_legal_actions()
        self.actions.set_actionGrid(actions)

        if state.button_index == 0:
            self.hero_button_pos()
        else:
            self.villain_button_pos()

        self.hero_hand.set_active(state.to_act_index == 0)
        self.villain_hand.set_active(state.to_act_index == 1)

        can_reset = (state.hand_over and (state.hero_stack == 0 or state.villain_stack == 0))
        self.reset_stacks.setEnabled(can_reset)
        self.next_hand.setEnabled(state.hand_over and not can_reset)


        recent_actions = state.actions_list
        self.action_history.set_actions(recent_actions)
        QTimer.singleShot(0, self.scroll_actions_to_end)
        
        QTimer.singleShot(500, lambda: self.board.set_board(state.board))




    def hero_button_pos(self) -> None: 
        self.dealer.setParent(self.hero_hand)
        self.dealer.move(0,0)
        self.dealer.show()

    def villain_button_pos(self) -> None: 
        self.dealer.setParent(self.villain_hand)
        self.dealer.move(0,0)
        self.dealer.show()

    def on_next_hand_clicked(self):
        # self.controller.state.button_index = (self.controller.state.button_index + 1) % 2
        self.controller.new_hand()
    
    def on_reset_stacks_clicked(self):
        self.controller.reset_stacks()

    def scroll_actions_to_end(self):
        bar = self.action_scroll.horizontalScrollBar()
        bar.setValue(bar.maximum())

    def eventFilter(self, obj, event):
        if obj == self.action_scroll.viewport() and event.type() == event.Type.Wheel:
            bar = self.action_scroll.horizontalScrollBar()
            bar.setValue(bar.value() - event.angleDelta().y())
            return True
        return super().eventFilter(obj, event)





