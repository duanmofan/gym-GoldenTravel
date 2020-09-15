# Deep-Q learning Agent
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.layers import Dense
import copy
import gym
class DQNAgent:
    def __init__(self, env):
        self.env = env
        self.memory = []
        self.gamma = 0.9  # decay rate
        self.epsilon = 1  # exploration
        self.epsilon_decay = .995
        self.epsilon_min = 0.1
        self.learning_rate = 0.0001
        self._build_model()
    
    def _build_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=6, activation='tanh'))
        model.add(Dense(128, activation='tanh'))
        model.add(Dense(128, activation='tanh'))
        model.add(Dense(2010, activation='linear'))
        model.compile(loss='mse',
                      optimizer=RMSprop(lr=self.learning_rate))
        self.model = model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return env.action_space.sample()
        act_values = self.model.predict(state)
        
        return np.argmax(act_values[0])  # returns action
    
    def replay(self, batch_size):
        batches = min(batch_size, len(self.memory))
        batches = np.random.choice(len(self.memory), batches)
        for i in batches:
            state, action, reward, next_state, done = self.memory[i]
            target = reward
            if not done:
              target = reward + self.gamma * \
                       np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            
            target_f[0][action] = target
            self.model.fit(state, target_f, nb_epoch=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
  

    env = gym.make('FuckCoding-v0')
    agent = DQNAgent(env)
    episodes=100

    import numpy as np
    rrrr = []
    for e in range(episodes):
#         agent.remember((26,30,20,8000,50,25), 2, 10000, (27,15,6,8000,50,24), False)
#         agent.remember((26,30,20,8000,50,25), 2, 10000, (27,15,6,8000,50,24), False)
#         agent.remember((26,30,20,8000,50,25), 2, 10000, (27,15,6,8000,50,24), False)
#         agent.remember((1,600,600,6000,1200,30), 6, 10000, (25,580,580,6000,1160,29), False)
#         agent.remember((1,600,600,6000,1200,30), 7, 10000, (25,580,580,6000,1160,29), False)
#         agent.remember((1,600,600,6000,1200,30), 9, 10000, (25,580,580,6000,1160,29), False)

        state = env.reset()
        state = np.reshape(state, [1, 6])
  

        actions = []
        states = []
        rewards = []
        
        for time_t in range(5000):
            # turn this on if you want to render
            # env.render()
  

            first_food = 1
            first_water = 1
            village_positions = []
            action = agent.act(state)
  

            actions.append(action)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 6])
            states.append(next_state)
            rewards.append(reward)

            
  

            agent.remember(state, action, reward, next_state, done)
  

            state = copy.deepcopy(next_state)
            

            if done:

                print("episode: {}/{}, score: {}"
                      .format(e, episodes, reward))
                print(actions)
                print(rewards)
                print(states)
                rrrr.append(reward)
                break
                

        agent.replay(32)
