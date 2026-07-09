from env.gd_env import GeometryDashEnv
from training.train import train
from game.renderer import Renderer
from ai.agent import Agent

if __name__ == "__main__":
    agent = Agent()
    Renderer().run_ai(agent)
