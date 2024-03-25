from stable_baselines3 import PPO
import os
from mazeenv2 import MazeEnv2
import time
from datetime import datetime
import numpy as np

# Following lines of code taken from website
now = datetime.now()
print("now =", now)
# dd/mm/YY H:M:S
dt_string = now.strftime("%b-%d-%Y-%H-%M")

# Original code:
##  models_dir = f"models/{int(time.time())}/"
##  logdir = f"logs/{int(time.time())}" + "_" + dt_string + "/"

# New code to run the model with "id" 1704253737:
models_dir = f"models/1704253737_3/40000.zip"
logdir = f"logs/1704253737_3 Test/"

# Checks to see if the paths exist, otherwise makes the path
#region
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)
#endregion

env = MazeEnv2()
env.reset()

# Changed this so it can load thing. Originally was:
# model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)
model = PPO.load(models_dir, env=env)

# This below has changed too, but I'm not too sure what it actually does.
episodes = 5

for ep in range(episodes):
    obs, info = env.reset()
    print(obs)
    done = False
    while not done:
        # for some reason obs has to be a numpy
        action, _states = model.predict(obs)
        obs, rewards, done, end_early, info = env.step(action)
        # env.render()
        print(rewards)
