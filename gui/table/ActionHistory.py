from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from .ActionHistoryBox import ActionHistoryBox
from controller.action import Action



class ActionHistory(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.items: list[QLabel] = []
        self.setFixedHeight(65)

        title = QLabel("ACTIONS")
        title.setStyleSheet("""QLabel {color: white; 
                            font-weight: bold;
                            padding: 8px; }""")
        self.layout.addWidget(title)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

    def add_action(self, action: Action) -> None:
        left_text, action_text = self.formatAction(action)
        chip = ActionHistoryBox(left_text, action_text)

        wrapper = QWidget()
        wrapper.setFixedHeight(chip.sizeHint().height() + 10)  # Add padding
        wrapper.setFixedWidth(chip.sizeHint().width() + 10)    # Add padding
        wrapper.setStyleSheet("background: transparent;")       # Make sure it's transparent

        wlay = QHBoxLayout(wrapper)
        wlay.setContentsMargins(0, 0, 0, 0)
        wlay.setSpacing(0)
        wlay.addWidget(chip)

        self.layout.addWidget(wrapper)
        self.items.append(wrapper)

        QTimer.singleShot(0, lambda: self._animate_chip_in_wrapper(wrapper, chip))
        self._scroll_to_end()



    def add_actions(self, actions: list[Action]) -> None:
        for action in actions:
            self.add_action(action)

    def clear_actions(self) -> None:
        for item in self.items:
            self.layout.removeWidget(item)
            item.deleteLater()
        self.items.clear()

    def set_actions(self, actions: list[Action]) -> None:
        if len(actions) == len(self.items):
            return
        
        if len(actions) > len(self.items):
            new_actions = actions[len(self.items):]
            
            # Create all widgets first but don't animate yet
            new_widgets = []
            for action in new_actions:
                left_text, action_text = self.formatAction(action)
                chip = ActionHistoryBox(left_text, action_text)

                wrapper = QWidget()
                wrapper.setFixedHeight(chip.sizeHint().height() + 10)
                wrapper.setFixedWidth(chip.sizeHint().width() + 10)
                wrapper.setStyleSheet("background: transparent;")

                wlay = QHBoxLayout(wrapper)
                wlay.setContentsMargins(0, 0, 0, 0)
                wlay.setSpacing(0)
                wlay.addWidget(chip)

                self.layout.addWidget(wrapper)
                self.items.append(wrapper)
                
                wrapper.hide()
                chip.hide()
                
                new_widgets.append((wrapper, chip))
            
            # Start animating the first widget
            if new_widgets:
                self._animate_sequence(new_widgets, 0)
        else:
            self.clear_actions()
            for action in actions:
                left_text, action_text = self.formatAction(action)
                chip = ActionHistoryBox(left_text, action_text)

                wrapper = QWidget()
                wrapper.setFixedHeight(chip.sizeHint().height() + 10)
                wrapper.setFixedWidth(chip.sizeHint().width() + 10)
                wrapper.setStyleSheet("background: transparent;")

                wlay = QHBoxLayout(wrapper)
                wlay.setContentsMargins(0, 0, 0, 0)
                wlay.setSpacing(0)
                wlay.addWidget(chip)

                self.layout.addWidget(wrapper)
                self.items.append(wrapper)
                chip.show()
                wrapper.show()
        
        self.adjustSize()
        self.updateGeometry()

        scroll = self.parentWidget()
        while scroll and not hasattr(scroll, "horizontalScrollBar"):
            scroll = scroll.parentWidget()

        if scroll:
            bar = scroll.horizontalScrollBar()
            bar.setValue(bar.maximum())

    def _animate_sequence(self, widgets_list, index):
        """Animate widgets one at a time in sequence"""
        if index >= len(widgets_list):
            return
        
        wrapper, chip = widgets_list[index]
        
        wrapper.show()
        chip.show()
        chip.raise_()
        
        start_pos = QPoint(120, 0)
        end_pos = QPoint(0, 0)
        chip.move(start_pos)

        slide = QPropertyAnimation(chip, b"pos", self)
        slide.setDuration(220)
        slide.setStartValue(start_pos)
        slide.setEndValue(end_pos)
        slide.setEasingCurve(QEasingCurve.Type.OutCubic)

        effect = QGraphicsOpacityEffect(chip)
        chip.setGraphicsEffect(effect)

        fade = QPropertyAnimation(effect, b"opacity", self)
        fade.setDuration(200)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        
        slide.finished.connect(lambda: [
            wrapper.setFixedWidth(chip.sizeHint().width() + 10),
            QTimer.singleShot(500, lambda: self._animate_sequence(widgets_list, index + 1))
        ])

        slide.start()
        fade.start()

        chip._slide_anim = slide
        chip._fade_anim = fade
        self._scroll_to_end()

    def formatAction(self, action: Action):
        if action.name in ("FLOP", "TURN", "RIVER"):
                cards_str = " ".join(str(c) for c in action.cards) if action.cards else ""
                return action.name, cards_str



        if action.name == "Post Blind":
            action_name = "BLIND"
        else:
            action_name = action.name.upper()

        if action.player == "villain":
            player = "VILLAIN"
        else:
            player = "HERO"

        left_text = f"{player}  {action.pot_after}"

        return left_text, action_name

    def _animate_chip_in(self, widget: QWidget):
        self.layout.activate()
        self.updateGeometry()

        widget.show()
        widget.raise_()

        end_pos = widget.pos()
        start_pos = QPoint(end_pos.x() + 120, end_pos.y())
        widget.move(start_pos)

        slide = QPropertyAnimation(widget, b"pos", self)
        slide.setDuration(500)
        slide.setStartValue(start_pos)
        slide.setEndValue(end_pos)
        slide.setEasingCurve(QEasingCurve.Type.OutCubic)

        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

        fade = QPropertyAnimation(effect, b"opacity", self)
        fade.setDuration(200)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)

        slide.start()
        fade.start()

        widget._slide_anim = slide
        widget._fade_anim = fade

    def _scroll_to_end(self):
        scroll = self.parentWidget()
        while scroll and not hasattr(scroll, "horizontalScrollBar"):
            scroll = scroll.parentWidget()

        if scroll:
            bar = scroll.horizontalScrollBar()
            bar.setValue(bar.maximum())

    def _animate_chip_in_wrapper(self, wrapper: QWidget, chip: QWidget):
        if hasattr(chip, '_animated'):
            return
        chip._animated = True
        
        wrapper.show()
        chip.show()
        chip.raise_()
        
        original_width = chip.sizeHint().width()
        
        start_pos = QPoint(120, 0)
        end_pos = QPoint(0, 0)
        chip.move(start_pos)

        slide = QPropertyAnimation(chip, b"pos", self)
        slide.setDuration(220)
        slide.setStartValue(start_pos)
        slide.setEndValue(end_pos)
        slide.setEasingCurve(QEasingCurve.Type.OutCubic)

        effect = QGraphicsOpacityEffect(chip)
        chip.setGraphicsEffect(effect)

        fade = QPropertyAnimation(effect, b"opacity", self)
        fade.setDuration(200)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        
        slide.finished.connect(lambda: wrapper.setFixedWidth(chip.sizeHint().width()))

        slide.start()
        fade.start()

        chip._slide_anim = slide
        chip._fade_anim = fade


