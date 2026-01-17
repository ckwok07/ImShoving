from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt, QTimer

from controller.decisionAccuracy import DecisionQuality
from .MoveListChip import MoveListChip

class MoveList(QWidget):
    def __init__(self):
        super().__init__()
        self.chips: list[MoveListChip] = []
        self._rendered_count = 0

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(6, 4, 6, 4)
        self.layout.setSpacing(6)

    def clear(self):
        while self.chips:
            chip = self.chips.pop()
            self.layout.removeWidget(chip)
            chip.deleteLater()
        self._rendered_count = 0

    def set_decisions(self, decisions: list[DecisionQuality]):
        # If a new hand starts and the engine resets decisions, clear UI.
        if len(decisions) < self._rendered_count:
            self.clear()

        # Add only the new decisions (assumes decisions is oldest -> newest)
        for d in decisions[self._rendered_count:]:
            chip = MoveListChip(
                d.label,
                d.accuracy,
                d.equity_before,
                d.hand,
                d.board
            )
            # Newest at top in the UI:
            self.layout.insertWidget(0, chip)
            self.chips.insert(0, chip)

        self._rendered_count = len(decisions)

