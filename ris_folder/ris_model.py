from stable_baselines3 import PPO, DDPG
import os
from ris_env import RisEnv
import time
from datetime import datetime

# Following lines of code taken from website
now = datetime.now()
print("now =", now)
# dd/mm/YY H:M:S
dt_string = now.strftime("%b-%d-%Y-%H-%M")


models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}" + "_" + dt_string + "-Ris_Rand_Pos_2/"

# Checks to see if the paths exist, otherwise makes the path
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = RisEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

# Will need to increase this... Since this kind of determines how long between each log.
TIMESTEPS = 2000
iters = 0
for i in range(1, 10000):
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS*iters}")