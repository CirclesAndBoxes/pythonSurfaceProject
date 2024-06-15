import gymnasium as gym
import numpy as np
from gymnasium import spaces


class RisEnv(gym.Env):
    """Custom Environment that follows gym interface."""
    # Idk what this is for
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super(RisEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Trying to use continuous space actions:
        #   https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html#tips-and-tricks-when-creating-a-custom-environment
        #   "Action space normalized and has interval range of 2. Gaussian distribution?"
        self.action_space = spaces.Box(low=-1, high=1, shape=(n_actions,), dtype="float32")
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-255, high=255,
                                            shape=(N_CHANNELS, HEIGHT, WIDTH), dtype=np.float32)

    def step(self, action):

        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        ...
        return observation, info

    def render(self):
        ...

    def close(self):
        ...