from game.engine import Engine

class GeometryDashEnv:
    def __init__(self):
        self.engine = Engine()

    def reset(self):
        return self.engine.reset()

    def step(self, action):
        return self.engine.step(action)

    def render(self):
        self.engine.render()
