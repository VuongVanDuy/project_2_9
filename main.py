import sys
import random
import math
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
        self.speed = random.uniform(1, 6)
        self.v_speed = 50

        self.a_velocity = QPointF(self.speed * math.cos(angle), self.speed * math.sin(angle))
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
            distance = line.length() / 30
            self.a_velocity += QPointF(distance * math.cos(self.angle), distance * math.sin(self.angle))
            self.setPos(self.pos() + self.a_velocity)
            self.current_pos = QPointF(self.x(), self.y())

            # Fade out
            self.setOpacity(self.opacity() - 0.08)
            if self.opacity() <= 0:
                self.scene().removeItem(self)

class FloatingImage(QGraphicsObject):
    def __init__(self, pixmap):
        super().__init__()
        self.pixmap = pixmap

        # Animation cho hiệu ứng bay
        self.animation = QPropertyAnimation(self, b'pos')
        self.animation.setDuration(8000)  # Thời gian di chuyển dài hơn để tạo hiệu ứng mềm mại hơn
        self.animation.setStartValue(QPointF(0, 0))
        self.animation.setEndValue(QPointF(600, 300))  # Tọa độ cuối cùng
        self.animation.setLoopCount(-1)  # Lặp lại liên tục

        # Thiết lập đường cong Bézier cho animation để tạo hiệu ứng chuyển động mượt mà và sinh động hơn
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

        # Điều chỉnh thêm các keyframe để tạo hiệu ứng bay phức tạp
        self.animation.setKeyValueAt(0.25, QPointF(150, 100))
        self.animation.setKeyValueAt(0.5, QPointF(300, 200))
        self.animation.setKeyValueAt(0.75, QPointF(450, 100))

    def boundingRect(self):
        return self.pixmap.rect().adjusted(-5, -5, 5, 5)  # Mở rộng vùng vẽ để thêm viền

    def paint(self, painter, option, widget=None):
        # Vẽ viền sáng xung quanh ảnh
        pen = QPen(QColor(255, 215, 0), 5)  # Viền màu vàng với độ rộng 5px
        painter.setPen(pen)
        painter.drawPixmap(0, 0, self.pixmap)


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

        #bk 1
        background_pixmap_left = QPixmap("vietnam.png")  # Change this to the path of your image
        scaled_pixmap_left = background_pixmap_left.scaled(self.scene.width() * 0.4, self.scene.height() * 0.5,
                                                 Qt.IgnoreAspectRatio)
        self.background_item_left = FloatingImage(scaled_pixmap_left)

        self.background_item_left.setPos(100, 100)
        self.scene.addItem(self.background_item_left)

        # Thêm background bản đồ
        background_pixmap = QPixmap("vietnam_map_vector.png")  # Change this to the path of your image
        scaled_pixmap = background_pixmap.scaled(self.scene.width() * 0.5, self.scene.height() * 0.9, Qt.IgnoreAspectRatio)
        self.background_item = QGraphicsPixmapItem(scaled_pixmap)

        x_pos = self.scene.width() - scaled_pixmap.width()
        self.background_item.setPos(x_pos, 0)
        self.background_item.setZValue(-1)  # Ensure the background is behind other items
        self.scene.addItem(self.background_item)

        # Initialize QMediaPlayer
        self.media_player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.media_player.setAudioOutput(self.audioOutput)
        self.media_player.setSource(QUrl.fromLocalFile("voice_audio.mp3"))
        self.audioOutput.setVolume(50)

        self.media_player.play()  # Play the music

        self.timer = QTimer()
        self.timer.timeout.connect(self.launch_firework)
        self.timer.start(200)  # Launch a firework every second
        self.add_congratulatory_text()

    def add_congratulatory_text(self):
        text_item = QGraphicsTextItem("Chúc Mừng Quốc Khánh Nước CHXHCN Việt Nam")
        font = QFont("Arial", 30, QFont.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(255, 215, 0))  # Gold color

        # Position the text at the center of the view
        text_item.setPos(20, 600)

        # Add a drop shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setOffset(5, 5)
        shadow_effect.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black shadow
        text_item.setGraphicsEffect(shadow_effect)

        # Add the text item to the scene
        self.scene.addItem(text_item)

        # Create a simple animation to make the text move up and down
        self.text_animation = QPropertyAnimation(text_item, b'pos')
        self.text_animation.setDuration(2000)
        self.text_animation.setLoopCount(-1)  # Loop indefinitely
        self.text_animation.setEasingCurve(QEasingCurve.InOutSine)
        self.text_animation.setStartValue(QPointF(text_item.x(), text_item.y()))
        self.text_animation.setEndValue(QPointF(text_item.x(), text_item.y() - 20))
        self.text_animation.start()

    def launch_firework(self):
        # Random position and color
        x = random.uniform(100, self.scene.width())
        y = random.uniform(200, self.scene.height())
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for i in range(1, 200):  # Number of particles
            deviation_x = random.uniform(-1, 1)
            deviation_y = random.uniform(-50, 0)
            angle = i * 2 * math.pi / 50
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
