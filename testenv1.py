import gym
import gym_xmoto
import time
env = gym.make('Xmoto-v0')

print("Env action space : ",env.action_space)
print("Env obs space : ",env.observation_space)

print("Agent starting in 3 seconds ...")
time.sleep(3)

for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        #print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print("Reward : " + str(reward))
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
