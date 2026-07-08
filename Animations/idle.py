import math


class IdleAnimation:
    def __init__(self,
                 amplitude=8,
                 frequency=0.06):
        self.t = 0.0
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = 0.0
        # Animation state
        self.bob = 0.0
        

    def update(self):
        self.t += self.frequency
        self.offset = math.sin(self.t) * self.amplitude
        return self.offset