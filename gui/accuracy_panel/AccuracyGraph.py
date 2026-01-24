from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QPointF, QRectF

class AccuracyGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # layout = QVBoxLayout(self)
        # layout.addWidget(QLabel("Accuracy Graph"))

        # self.setStyleSheet("""QWidget {background: #191919;
        #                    color: white;}""")

        self.values: list[list[float]] = []
        self.setStyleSheet("background: #0b0b0b; border-radius: 6px;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(260)
        

        self.margin_left = 20
        self.margin_bottom = 20
        self.margin_top = 20
        self.margin_right = 10
    
    def set_data(self, values: list[list[float]]):
        self.values = values
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 6, 6)
        painter.setClipPath(path)

        self.draw_background(painter)
        self.draw_grid(painter)
        self.draw_axes(painter)
        self.draw_curve(painter)

        painter.end()
    
    def draw_background(self, painter):
        painter.fillRect(self.rect(), QColor("#0b0b0b"))
    
    def draw_grid(self, painter):
        pen = QPen(QColor("#2a2a2a"), 1, Qt.PenStyle.DotLine)
        painter.setPen(pen)

        graph_w = self.width() - self.margin_left - self.margin_right
        graph_h = self.height() - self.margin_top - self.margin_bottom

        # vertical grid
        for i in range(1, 6):
            x = self.margin_left + i * graph_w / 6
            painter.drawLine(int(x), self.margin_top, int(x), self.margin_top + graph_h)

        # horizontal grid
        for i in range(1, 5):
            y = self.margin_top + i * graph_h / 5
            painter.drawLine(self.margin_left, int(y), self.margin_left + graph_w, int(y))

    
    def draw_axes(self, painter):
        pen = QPen(QColor("#888888"), 1)
        painter.setPen(pen)

        x0 = self.margin_left
        y0 = self.height() - self.margin_bottom
        x1 = self.width() - self.margin_right
        y1 = self.margin_top

        painter.drawLine(x0, y0, x1, y0)  # X axis
        painter.drawLine(x0, y0, x0, y1)  # Y axis

    def draw_curve(self, painter):
        if len(self.values) == 0:
            return

        w = self.width() - self.margin_left - self.margin_right
        h = self.height() - self.margin_top - self.margin_bottom

        min_val = 0
        span = 100

        # avg_accuracy, raw_accuracy, rolling_accuracy
        colors = [QColor("#ffa500"), QColor("#7ce7e1"), QColor("#d6d6d6")]

        for series_index, series in enumerate(self.values):
            if len(series) == 0:
                continue

            pen = QPen(colors[series_index % len(colors)], 1.5)
            painter.setPen(pen)

            if len(series) == 1:
                v = series[0]
                x = self.margin_left + w / 2
                y = self.margin_top + (1 - v / span) * h
                painter.drawEllipse(QPointF(x, y), 3, 3)
                continue

            points = []
            for i, v in enumerate(series):
                x = self.margin_left + (i / (len(series) - 1)) * w
                y = self.margin_top + (1 - (v - min_val) / span) * h
                points.append(QPointF(x, y))

            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i + 1])

class LegendWidget(QWidget):
    def __init__(self, labels: list[str], colors: list[str]):
        super().__init__()
        self.labels = labels
        self.colors = colors
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 5, 10, 5)
        layout.setSpacing(30)
        
        for label, color in zip(self.labels, self.colors):
            item_layout = QHBoxLayout()
            item_layout.setSpacing(8)
            
            # Color indicator
            color_widget = QWidget()
            color_widget.setFixedSize(20, 3)
            color_widget.setStyleSheet(f"background-color: {color}; border-radius: 1px;")
            
            # Label text
            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #cccccc; font-size: 11px;")
            
            item_layout.addWidget(color_widget)
            item_layout.addWidget(label_widget)
            
            layout.addLayout(item_layout)
        
        layout.addStretch()
        self.setStyleSheet("background: transparent;")
