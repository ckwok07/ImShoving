from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve


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

        if len(decisions) < self._rendered_count:
            self.clear()

        for d in decisions[self._rendered_count:]:
            chip = MoveListChip(d.label,d.accuracy,d.equity_before,d.hand,d.board)

            self.layout.insertWidget(0, chip)
            self.chips.insert(0, chip)

            self._animate_chip_in(chip)


        self._rendered_count = len(decisions)

    def _animate_chip_in(self, chip: MoveListChip):
        QTimer.singleShot(0, lambda: self._run_animation(chip))


    def _run_animation(self, chip: MoveListChip):
        final_pos = chip.pos()

        effect = QGraphicsOpacityEffect(chip)
        chip.setGraphicsEffect(effect)

        fade = QPropertyAnimation(effect, b"opacity", chip)
        fade.setDuration(180)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.start()

        chip._fade_anim = fade


        offset = 25
        start_pos = QPoint(final_pos.x(), final_pos.y() - offset)

        chip.move(start_pos)

        anim = QPropertyAnimation(chip, b"pos", chip)
        anim.setDuration(180)
        anim.setStartValue(start_pos)
        anim.setEndValue(final_pos)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        chip._anim = anim
        anim.start()
