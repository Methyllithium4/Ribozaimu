from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt


class Renderer:

    def __init__(self):
        self.sprite = QPixmap("Sprites/idle1.png")

    def draw(self, widget, anim, pos):

        painter = QPainter(widget)

        x = pos.x() - self.sprite.width() // 2
        y = pos.y() - self.sprite.height() // 2 + anim.bob

        painter.drawPixmap(x, y, self.sprite)
        painter.end()