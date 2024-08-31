import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

class HeartWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Thiết lập bút vẽ
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)

        # Lấy kích thước khung vẽ
        width = self.size().width()
        height = self.size().height()

        # Tạo giá trị tham số t
        t = np.linspace(0, 2 * np.pi, 1000)

        # Tính giá trị của x và y
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

        # Chuyển đổi tọa độ để phù hợp với kích thước khung vẽ
        x = (x - np.min(x)) / (np.max(x) - np.min(x)) * width
        y = (y - np.min(y)) / (np.max(y) - np.min(y)) * height

        # Vẽ đường cong trái tim
        for i in range(len(t) - 1):
            painter.drawLine(int(x[i]), int(height - y[i]), int(x[i+1]), int(height - y[i+1]))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Heart Shape with PySide6")
        self.setFixedSize(300, 400)

        # Tạo widget chính và thiết lập layout
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Thêm widget vẽ trái tim vào layout
        heart_widget = HeartWidget()
        layout.addWidget(heart_widget)

        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
