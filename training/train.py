from env.gd_env import GeometryDashEnv
from ai.agent import Agent
import config

def train():
    env = GeometryDashEnv()
    agent = Agent()

    for episode in range(config.EPISODES):
        state = env.reset()
        total_reward = 0

        while True:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)

            agent.store(state, action, reward, next_state, done)
            agent.train()

            state = next_state
            total_reward += reward

            if done:
                print(f"Episode {episode} | Reward: {total_reward}")
                break

if __name__ == "__main__":
    train()
