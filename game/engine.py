import os
from game.player import Player
from game.level import Level

class Engine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.level = Level()
        self.x = 0
        self.done = False
        return self.get_state()

    def get_state(self):
        next_spike = min([s.x for s in self.level.spikes if s.x >= self.x], default=200)
        distance = next_spike - self.x
        return [self.player.y, self.player.velocity, distance]

    def step(self, action):
        if action == 1:
            self.player.jump()

        self.player.update()
        self.x += 1

        for spike in self.level.spikes:
            if abs(self.x - spike.x) < 2 and self.player.y == 0:
                self.done = True

        reward = 1
        if self.done:
            reward = -100

        return self.get_state(), reward, self.done

    def render(self, width=40, height=12, player_col=5):
        def clear_console():
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")

        clear_console()
        ground_row = height - 1
        screen = [[" " for _ in range(width)] for _ in range(height)]

        for x in range(width):
            screen[ground_row][x] = "_"

        for spike in self.level.spikes:
            rel_x = spike.x - self.x
            if 0 <= rel_x < width:
                screen[ground_row - 1][rel_x] = "^"

        player_row = ground_row - min(int(round(self.player.y)), height - 2)
        player_row = max(0, player_row)

        if 0 <= player_col < width:
            if screen[player_row][player_col] == "^":
                screen[player_row][player_col] = "X"
            else:
                screen[player_row][player_col] = "P"

        status = f"X={self.x} Y={self.player.y:.1f} V={self.player.velocity} done={self.done}"
        output_lines = [status] + ["".join(row) for row in screen]
        print("\n".join(output_lines))
