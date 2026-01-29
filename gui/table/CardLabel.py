from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer, QPoint

from main.model.Card import Card
from main.model.Rank import Rank
from main.model.Suit import Suit

class CardLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""QLabel {background-color: #2b2b2b;
                           border-radius: 6px;}""")
        
        self.setFixedSize(75, 105)
        
        self.card = None
        self.face_up = True
        
    def set_card(self, card: Card, face_up=True, animate=False, delay=0):
        self.card = card
        self.face_up = face_up
        
        if animate:
            if delay > 0:
                QTimer.singleShot(delay, lambda: self._refresh_and_animate())
            else:
                QTimer.singleShot(0, lambda: self._refresh_and_animate())
        else:
            self.refresh()

    def _refresh_and_animate(self):
        self.refresh()
    
        temp_pixmap = self.pixmap()
        self.setPixmap(QPixmap()) 
        
        self._run_animation(temp_pixmap)

    def _run_animation(self, card_pixmap):
        if not card_pixmap:
            return
            
        temp_label = QLabel(self.parent())
        temp_label.setPixmap(card_pixmap)
        temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temp_label.setStyleSheet("background: transparent; border: none;")
        temp_label.setFixedSize(self.size())
        
        global_pos = self.mapToGlobal(QPoint(0, 0))
        parent_pos = self.parent().mapFromGlobal(global_pos)
        temp_label.move(parent_pos)
        temp_label.raise_()
        temp_label.show()
        
        effect = QGraphicsOpacityEffect(temp_label)
        temp_label.setGraphicsEffect(effect)
        
        fade = QPropertyAnimation(effect, b"opacity", temp_label)
        fade.setDuration(300)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        offset = 30
        start_pos = QPoint(parent_pos.x(), parent_pos.y() - offset)
        temp_label.move(start_pos)
        
        slide = QPropertyAnimation(temp_label, b"pos", temp_label)
        slide.setDuration(300)
        slide.setStartValue(start_pos)
        slide.setEndValue(parent_pos)
        slide.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        def finish_animation():
            self.setPixmap(card_pixmap)
            temp_label.deleteLater()
        
        slide.finished.connect(finish_animation)
        
        fade.start()
        slide.start()

        temp_label._fade_anim = fade
        temp_label._slide_anim = slide

    def hide_card(self):
        self.face_up = False
        self.refresh()

    def show_card(self):
        self.face_up = True
        self.refresh()

    def clear(self):
        self.card = None
        self.setPixmap(QPixmap())

    def refresh(self):
        if not self.card:
            self.clear()
            return

        if self.face_up:
            filename = f"assets/cards/{self.card}.png"
        else:
            filename = "assets/cards/back.png"

        pixmap = QPixmap(filename)

        dpr = self.devicePixelRatioF()

        margin = 2
        target_size = QSize(
            int((self.width() - margin * 2) * dpr),
            int((self.height() - margin * 2) * dpr))

        scaled = pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)

        scaled.setDevicePixelRatio(dpr)
        self.setPixmap(scaled)