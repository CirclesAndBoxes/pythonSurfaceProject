from stable_baselines3 import PPO, DDPG
import os
from ris_env import RisEnv
from ris_env_const import RisEnvConst
import time
from datetime import datetime

# Following lines of code taken from website

models_dir_past = f"models/1720497686"
models_dir = f"models/1720497686_(2)"
logdir = f"logs/1720497686_(2)-Log"

# Checks to see if the paths exist, otherwise makes the path
if not os.path.exists(models_dir):
    print("No Model Path")
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    print("No Log Path")
    os.makedirs(logdir)

env = RisEnvConst()
env.reset()

model = PPO.load(models_dir_past + "/1419000.zip", env=env, verbose=1, tensorboard_log=logdir)
model.set_parameters(load_path_or_dict=(models_dir_past+"/1419000.zip"))
# Will need to increase this... Since this kind of determines how long between each log.
TIMESTEPS = 10000
iters = 0
for i in range(1, 10000):
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS*iters}")