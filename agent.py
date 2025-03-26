import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from game import get_state, init, play_step

record = 0

# parameters
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.epsilon = -1
        self.gamma = 0.8
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(5, 64, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def get_state(self):
        state = get_state()
        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        return self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        return self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        move = [0, 0]
        if random.randint(0, 100) < self.epsilon:
            move[random.randint(0, 1)] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            with torch.no_grad():
                prediction = self.model(state0)
                move[torch.argmax(prediction).item()] = 1

        return move

def train():
    init()
    agent = Agent()
    while True:
        global record
        state_old = agent.get_state()
        move = agent.get_action(state_old)
        score, reward, done = play_step(move, record)
        state_new = agent.get_state()

        # train short memory
        agent.train_short_memory(state_old, move, reward, state_new, done)

        # remember
        agent.remember(state_old, move, reward, state_new, done)

        if done:
            loss = agent.train_long_memory()
            print(loss)
            if record < score:
                record = score
                agent.model.save('cpu.pth')
            init()

def test():
    init()
    agent = Agent()
    agent.model.load('cpu.pth')
    while True:
        global record
        move = [0, 0]
        state = agent.get_state()
        state = torch.tensor(state, dtype=torch.float)
        with torch.no_grad():
            prediction = agent.model(state)
            move[torch.argmax(prediction).item()] = 1
        
        score, _, done = play_step(move, record)

        if done:
            if record < score:
                record = score
            init()


if __name__ == '__main__':
    test()