# Whole point of this file is to check to see if our snake environment works with stable_baseline3

from stable_baselines3.common.env_checker import check_env
from ris_env_const import RisEnv
env = RisEnv()

check_env(env)
