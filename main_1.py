import sys
import random
import numpy as np
from PySide6.QtCore import Qt, QTimer, QPointF, QLineF, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QBrush, QColor, QPainter, QPixmap, QPen, QPainterPath, QFont
from PySide6.QtWidgets import QApplication, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsObject, QGraphicsTextItem, QGraphicsDropShadowEffect
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

class FireworkParticle(QGraphicsEllipseItem):
    def __init__(self, root_pos, deviation, angle, color):
        super().__init__(-2, -2, 4, 4)
        self.setBrush(QBrush(color))
        self.root_pos = root_pos
        self.setPos(root_pos - deviation)
        self.setOpacity(1.0)

        self.timer = 0
        self.angle = angle
        self.speed = random.uniform(1, 1.5)
        self.v_speed = 50

        self.d_x = 16 * np.sin(self.angle)**3
        self.d_y = 13 * np.cos(self.angle) - 5 * np.cos(2*self.angle) - 2 * np.cos(3*self.angle) - np.cos(4*self.angle)
        self.a_velocity = QPointF(self.speed * self.d_x, self.speed * self.d_y)
        self.v_velocity = QPointF(0, self.v_speed)

    def advance(self, phase):
        if phase == 0:
            return

        # Move the particle
        if self.timer < 5:
            line = QLineF(self.root_pos, self.pos())
            distance = line.length() / 5

            self.v_velocity -= QPointF(0, distance)
            self.setPos(self.pos() - self.v_velocity)
            self.current_pos = QPointF(self.x(), self.y())
            self.before_explos_pos = self.current_pos
            self.timer += 1
        else:
            line = QLineF(self.before_explos_pos, self.current_pos)
            distance = line.length() / 100
            self.a_velocity += QPointF(distance * self.d_x, distance * self.d_y)
            self.setPos(self.pos() - self.a_velocity)
            self.current_pos = QPointF(self.x(), self.y())

            # Fade out
            self.setOpacity(self.opacity() - 0.15)
            if self.opacity() <= 0:
                self.scene().removeItem(self)


class Firework(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 700)

        # Thiết lập kích thước của QGraphicsView (cùng kích thước với scene)
        self.setFixedSize(1000, 700)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QBrush(Qt.black))


        self.timer = QTimer()
        self.timer.timeout.connect(self.launch_firework)
        self.timer.start(200)  # Launch a firework every second

    def launch_firework(self):
        # Random position and color
        x = random.uniform(100, self.scene.width())
        y = random.uniform(200, self.scene.height())
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for i in range(1, 200):  # Number of particles
            deviation_x = random.uniform(-1, 1)
            deviation_y = random.uniform(-50, 0)
            angle = i * 2 * np.pi / 50
            particle = FireworkParticle(QPointF(x, y),
                                        QPointF(deviation_x, deviation_y),
                                        angle, color)
            self.scene.addItem(particle)

        # Start the animation
        self.scene.advance()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    firework = Firework()
    #firework.setSceneRect(0, 0, 800, 600)
    firework.setWindowTitle("Firework Simulation")
    firework.show()
    sys.exit(app.exec())
