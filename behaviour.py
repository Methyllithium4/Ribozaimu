import math
from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtGui import QCursor


class BehaviourController(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.t = 0.0
        self.bob = 0.0

        self.facing_right = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def update(self):
        self.t += 0.08

        # bobbing
        self.bob = math.sin(self.t) * 5

        self.update_facing_direction()

    def update_facing_direction(self):
        cursor_x = QCursor.pos().x()
        window_center_x = self.window.x() + (self.window.width() // 2)

        self.facing_right = cursor_x > window_center_x

    def get_bob_offset(self):
        return self.bob

    # NEW: normalized phase for animation cycling
    def get_anim_phase(self):
        return (math.sin(self.t) + 1) / 2  # 0 → 1

    def is_facing_right(self):
        return self.facing_right