import gymnasium as gym
from stable_baselines3 import PPO

# Whole point of this file is to check to see if our snake environment works with stable_baseline3

from stable_baselines3.common.env_checker import check_env
from mazeenv import MazeEnv
env = MazeEnv()

# env = gym.make('LunarLander-v2', render_mode='human')  # continuous: LunarLanderContinuous-v2
# print("hello.....")
# env = gym.make('LunarLander-v2', render_mode='human')
env.reset()
# print("env:", env)
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./ppo/")
model.learn(total_timesteps=100000)

# for step in range(200):
#     env.render()
#     # take random action
#     obs, reward, done, info, test1 = env.step(env.action_space.sample())
#     print(reward, done)

episodes = 10
for ep in range(episodes):
    obs = env.reset()
    print("env:", env)
    done = False
    while not done:
        # pass observation model to get predicted action
        action, _states = model.predict(obs)

        # pass action to env and get info back
        obs, rewards, done, info = env.step(action)

        # show the environment on the screen
        env.render()
env.close()
