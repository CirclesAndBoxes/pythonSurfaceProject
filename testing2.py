import gym
from stable_baselines3 import PPO

env = gym.make('LunarLander-v2', render_mode="human")  # continuous: LunarLanderContinuous-v2
env.reset()
print("env.observation_space", env.observation_space)
for step in range(200):
	env.render()
	# take random action
	obs, reward, done, truncated, info = env.step(0)
	print(reward, done)

env.close()
print("aaaa")