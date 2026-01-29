from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt, QPointF, QRectF
from gui.table.CardLabel import CardLabel
from main.model.Card import Card

LABEL_COLOUR = {95: "#26c2a3", 
                  85: "#749bbf", 
                  70: "#81b64c",
                  60: "#f7c631", 
                  40: "#ffa459", 
                  0: "#fa412d" }

class MoveListChip(QWidget):
    def __init__(self, quality: str = "",
                  accuracy: float = 0.0, 
                  ev_chosen: float = 0.0,
                  action_name: str = "",
                  action_size: str = "",
                  best_action: str = "",
                  ev_best: float = 0.0,
                  equity: float  = 0.0, 
                  hand: list[Card] | None = None, 
                  board: list[Card] | None = None):
        super().__init__()


        hand = hand or []
        board = board or []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)
        layout.setSpacing(6)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.chip = QWidget()
        chip_layout = QVBoxLayout(self.chip)
        chip_layout.setContentsMargins(8, 3, 8, 8)
        chip_layout.setSpacing(4)

        top_row = QHBoxLayout()
        second_row = QHBoxLayout()
        second_row.setSpacing(2)
        top_row.setContentsMargins(0, 0, 0, 0)
        second_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(6)
        second_row.setSpacing(2)

        self.quality_label = QLabel()
        self.ev_label = QLabel()
        self.accuracy_label = QLabel()

        top_row.addWidget(self.quality_label)
        top_row.addWidget(self.accuracy_label)
        second_row.addWidget(self.ev_label)

        self.equity = QWidget()
        equity_layout = QVBoxLayout(self.equity)
        self.hand_cards_layout = QHBoxLayout()
        self.board_cards_layout = QHBoxLayout()
        self.equity.setStyleSheet("""QWidget { background-color: #2f2f2f;
                                border-radius: 6px;
                                padding: 0px; }""")

        self.hand_cards_layout.setSpacing(2)
        self.board_cards_layout.setSpacing(2)

        self.hand_cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.board_cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(4)
        grid.setColumnMinimumWidth(1, 153)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 0)

        hand_label = QLabel("HAND")
        board_label = QLabel("BOARD")

        grid.addWidget(hand_label, 0, 0)
        grid.addWidget(board_label, 0, 1)

        grid.addLayout(self.hand_cards_layout, 1, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addLayout(self.board_cards_layout, 1, 1, Qt.AlignmentFlag.AlignLeft)


        equity_layout.addLayout(grid)

        self.equity_label = QLabel()

        equity_layout.addWidget(self.equity_label)

        chip_layout.addLayout(top_row)
        chip_layout.addLayout(second_row)
        chip_layout.addWidget(self.equity)

        self.best_choice = QLabel(f"BEST: {best_action} - EV: {ev_best:.1f}")
        chip_layout.addWidget(self.best_choice)

        layout.addWidget(self.chip)

        self.setStyleSheet("""
            QWidget {
                background: #3a3a3a;
                border-radius: 10px;
                padding: 6px;
            }
            QLabel {
                color: #bbbbbb;
                font-size: 12px;
                font-weight: bold;
            }""")
            

        self.set_data(quality, 
                      accuracy, 
                      ev_chosen, 
                      action_name, 
                      action_size, 
                      best_action,
                      ev_best,
                      equity, 
                      hand, 
                      board)

    def set_data(self, quality: str, 
                 accuracy: float, 
                 ev_chosen: float,
                 action_name : str, 
                 action_size: str, 
                 best_action: str,
                 ev_best: float,
                 equity: float, 
                 hand: list[Card], 
                 board: list[Card]):
        
        self._hand = list(hand)
        self._board = list(board)

        if action_size == "0.00":
            self.quality_label.setText(f"{quality.upper()}: {action_name.upper()}")
        else:
            self.quality_label.setText(f"{quality.upper()}: {action_name.upper()} {action_size}")
        self.ev_label.setText(f"EV: {ev_chosen:.1f}")
        self.accuracy_label.setText(f"ACCURACY: {accuracy:.0f}%")
        self.best_choice.setText(f"BEST: {best_action} - EV: {ev_best:.1f}")

        self._clear_layout(self.hand_cards_layout)
        self._clear_layout(self.board_cards_layout)

        for card in self._hand:
            lbl = CardLabel()
            lbl.setStyleSheet("""QLabel { background: transparent;
                            border-radius: 2px; 
                            border: 3px solid #2b2b2b; }""")
            lbl.setFixedSize(28, 38)
            lbl.set_card(card)
            self.hand_cards_layout.addWidget(lbl)

        for card in self._board:
            lbl = CardLabel()
            lbl.setStyleSheet("""QLabel { background: transparent;
                            border-radius: 3px; 
                            border: 3px solid #2b2b2b; }""")
            lbl.setFixedSize(28, 38)
            lbl.set_card(card)
            self.board_cards_layout.addWidget(lbl)


        equity_label_text = f"EQUITY: {equity * 100:.1f}%"
        self.equity_label.setText(equity_label_text)

        color = self.get_color(accuracy)
        self.quality_label.setStyleSheet(f"color: {color};")

    def get_color(self, accuracy: float) -> str:
        for threshold in sorted(LABEL_COLOUR.keys(), reverse=True):
            if accuracy >= threshold:
                return LABEL_COLOUR[threshold]
        return "#bbbbbb"
    
    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()