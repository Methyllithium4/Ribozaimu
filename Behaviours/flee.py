from PySide6.QtCore import QPointF
import math

class FleeBehaviour:
    def __init__(self):
        self.position = QPointF()
        self.velocity = QPointF()

        self.max_speed = 900.0          # px/s
        self.acceleration = 2500.0      # px/s²
        self.friction = 5.5

        self.fear_radius = 220.0
        self.teleport_radius = 60.0

        self.home = QPointF()

    def set_position(self, pos):
        self.position = QPointF(pos)

    def set_home(self, pos):
        self.home = QPointF(pos)

    def update(self, dt, mouse_pos, screen_rect, alt_pressed):
        if alt_pressed:
            # Slowly drift back toward home.
            dx = self.home.x() - self.position.x()
            dy = self.home.y() - self.position.y()

            self.velocity.setX(self.velocity.x() + dx * dt * 2.0)
            self.velocity.setY(self.velocity.y() + dy * dt * 2.0)

        else:
            dx = self.position.x() - mouse_pos.x()
            dy = self.position.y() - mouse_pos.y()

            dist = math.hypot(dx, dy)

            if 1 < dist < self.fear_radius:
                strength = (self.fear_radius - dist) / self.fear_radius

                dx /= dist
                dy /= dist

                self.velocity.setX(
                    self.velocity.x() + dx * self.acceleration * strength * dt
                )

                self.velocity.setY(
                    self.velocity.y() + dy * self.acceleration * strength * dt
                )

        # Friction
        self.velocity *= max(0.0, 1.0 - self.friction * dt)

        # Clamp speed
        speed = math.hypot(self.velocity.x(), self.velocity.y())
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity *= scale

        # Move
        self.position += self.velocity * dt

        # Teleport if cornered
        if not alt_pressed:
            x = self.position.x()
            y = self.position.y()

            if (
                x < 10
                or x > screen_rect.width() - 10
                or y < 10
                or y > screen_rect.height() - 10
            ):
                dx = self.position.x() - mouse_pos.x()
                dy = self.position.y() - mouse_pos.y()

                if math.hypot(dx, dy) < self.teleport_radius:
                    self.position.setX(
                        screen_rect.width() - x
                    )
                    self.position.setY(
                        screen_rect.height() - y
                    )

        return self.position