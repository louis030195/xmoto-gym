import gym
import gym_xmoto
env = gym.make('Xmoto-v0')
env.render(accelerated=False)
try:
    for _ in range(1000):
        state, reward, done, info = env.step(env.action_space.sample()) # take a random action
        print('info {}'.format(info))

finally: # Need to do a clean close
    env.close()