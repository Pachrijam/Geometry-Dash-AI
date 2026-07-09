import pygame
import os
from game.engine import Engine

WIDTH = 800
HEIGHT = 400
GROUND_Y = 300

class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Geometry Dash AI")
        self.clock = pygame.time.Clock()
        self.engine = Engine()

        project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        assets_dir = os.path.join(project_root, "assets")

        if not os.path.isdir(assets_dir):
            assets_dir = os.path.abspath(os.path.join(project_root, "..", "assets"))

        if not os.path.isdir(assets_dir):
            raise FileNotFoundError(
                f"Assets directory not found. Checked: {project_root + os.sep + 'assets'} and {os.path.abspath(os.path.join(project_root, '..', 'assets'))}"
            )

        # Load assets
        self.bg = pygame.image.load(os.path.join(assets_dir, "background.png")).convert()
        self.player = pygame.image.load(os.path.join(assets_dir, "icon.png")).convert_alpha()
        self.ground = pygame.image.load(os.path.join(assets_dir, "ground.png")).convert()

        # Scale assets
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.player = pygame.transform.scale(self.player, (40, 40))
        self.ground = pygame.transform.scale(self.ground, (WIDTH, 40))

        self.rotation = 0

    def draw(self):
        # 🎯 Scrolling background
        bg_x = -(self.engine.x % WIDTH)
        self.screen.blit(self.bg, (bg_x, 0))
        self.screen.blit(self.bg, (bg_x + WIDTH, 0))

        # 🎯 Player rotation (Geometry Dash feel)
        self.rotation += 5
        rotated = pygame.transform.rotate(self.player, self.rotation)

        player_y = GROUND_Y - self.engine.player.y - 40
        self.screen.blit(rotated, (100, player_y))

        # 🎯 Ground
        self.screen.blit(self.ground, (0, GROUND_Y + 20))

        # 🔺 Spikes (keep your old ones for now)
        for spike in self.engine.level.spikes:
            screen_x = spike.x - self.engine.x + 100
            if 0 < screen_x < WIDTH:
                pygame.draw.polygon(
                    self.screen,
                    (255, 0, 0),
                    [
                        (screen_x, GROUND_Y + 20),
                        (screen_x + 10, GROUND_Y),
                        (screen_x + 20, GROUND_Y + 20),
                    ],
                )

        pygame.display.flip()

    def run_ai(self, agent):
        running = True
        state = self.engine.reset()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            action = agent.choose_action(state)
            state, _, done = self.engine.step(action)

            if done:
                state = self.engine.reset()

            self.draw()
            self.clock.tick(60)

        pygame.quit()