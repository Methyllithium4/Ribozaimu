import math


class Animation:

    def __init__(self):
        self.t = 0.0
        self.bob = 0

    def update(self):
        self.t += 0.05
        self.bob = math.sin(self.t) * 6