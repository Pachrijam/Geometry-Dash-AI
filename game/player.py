class Player:
    def __init__(self):
        self.y = 0
        self.velocity = 0
        self.gravity = -1
        self.jump_strength = 10

    def jump(self):
        if self.y == 0:
            self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = 0
