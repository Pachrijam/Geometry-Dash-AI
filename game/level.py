from game.objects import Spike

class Level:
    def __init__(self):
        self.spikes = [Spike(x) for x in range(20, 200, 40)]
