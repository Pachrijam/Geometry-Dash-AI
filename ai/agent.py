import torch
import torch.optim as optim
import random
from collections import deque
from ai.model import Model
import config

class Agent:
    def __init__(self):
        self.model = Model()
        self.optimizer = optim.Adam(self.model.parameters(), lr=config.LR)
        self.memory = deque(maxlen=10000)
        self.epsilon = config.EPSILON

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 1)

        state = torch.FloatTensor(state)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def store(self, s, a, r, ns, d):
        self.memory.append((s, a, r, ns, d))

    def train(self, batch_size=32):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)

        for s, a, r, ns, d in batch:
            s = torch.FloatTensor(s)
            ns = torch.FloatTensor(ns)

            target = r
            if not d:
                target += config.GAMMA * torch.max(self.model(ns)).item()

            output = self.model(s)[a]

            loss = (output - target) ** 2

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        if self.epsilon > config.EPSILON_MIN:
            self.epsilon *= config.EPSILON_DECAY
