# Taken directly from: https://pythonprogramming.net/custom-environment-reinforcement-learning-stable-baselines-3-tutorial/

from stable_baselines3 import PPO
import os
from copiedsnake import SnekEnv
import time
#Following taken from https://www.programiz.com/python-programming/datetime/current-datetime
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%b-%d-%Y-%H-%M")

#End citation


models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}" + "_" + dt_string + "/"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = SnekEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
iters = 0
for i in range(1, 10000000):
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS*iters}")