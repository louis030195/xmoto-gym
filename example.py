import gym
import gym_xmoto
env = gym.make('Xmoto-v0')
env.render(False)
for _ in range(1000):
    env.step(env.action_space.sample()) # take a random action