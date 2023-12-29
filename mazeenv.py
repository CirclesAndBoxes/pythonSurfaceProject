import gymnasium as gym
import numpy as np
from gymnasium import spaces
import cv2
import random
import time

maze = [[1, 0, 1, 2, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 1, 1, 1]]

def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_position, score

def collision_with_boundaries(snake_head):
    if snake_head[0] >= 490 or snake_head[0] < 0 or snake_head[1] >= 490 or snake_head[1] < 0:
        return 1
    else:
        return 0

def collision_with_maze(position):
    if position[0] > len(maze):
        return True
    elif position[1] > len(maze[0]):
        return True
    elif position[0] < 0:
        return True
    elif position[1] < 0:
        return True
    elif maze[position[0]][position[1]] == 1:
        return True
    else:
        return False

class MazeEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super(MazeEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-20, high=500,
                                            shape=(2,), dtype=np.int32)

    def step(self, action):
        cv2.imshow('a', self.img)
        cv2.waitKey(1)
        img = np.zeros((490, 490, 3), dtype='uint8')
        # Display Apple
        cv2.rectangle(img, (self.apple_position[0], self.apple_position[1]), (self.apple_position[0] + 70, self.apple_position[1] + 70),
                      (0, 0, 255), 3)
        # Display player

        cv2.rectangle(img, (self.seen_position[0], self.seen_position[1]), (self.seen_position[0] + 70, self.seen_position[1] + 70),
                      (0, 255, 0), 3)

        # Display Maze:

        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 1:
                    cv2.rectangle(img, (j * 70, i * 70), (j * 70 + 70, i * 70 + 70),
                                  (255, 255, 255), 3)

        # Action
        button_direction = action

        # Change the position based on the button direction
        if button_direction == 1:
            self.seen_position[0] += 70
            self.player_pos[1] += 1
        elif button_direction == 0:
            self.seen_position[0] -= 70
            self.player_pos[1] -= 1
        elif button_direction == 2:
            self.seen_position[1] += 70
            self.player_pos[0] += 1
        elif button_direction == 3:
            self.seen_position[1] -= 70
            self.player_pos[0] -= 1

        # End game when reaching ends
        if self.seen_position == self.apple_position:
            font = cv2.FONT_HERSHEY_SIMPLEX
            img = np.zeros((490, 490, 3), dtype='uint8')
            cv2.putText(img, 'You win!', (140, 250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('a', img)
            cv2.waitKey(0)
            self.done = True

        # On collision "undo"
        if collision_with_boundaries(self.seen_position) == 1:
            if button_direction == 1:
                self.seen_position[0] += -70
                self.player_pos[1] += -1
            elif button_direction == 0:
                self.seen_position[0] -= -70
                self.player_pos[1] -= -1
            elif button_direction == 2:
                self.seen_position[1] += -70
                self.player_pos[0] += -1
            elif button_direction == 3:
                self.seen_position[1] -= -70
                self.player_pos[0] -= -1
        elif collision_with_maze(self.player_pos):
            if button_direction == 1:
                self.seen_position[0] += -70
                self.player_pos[1] += -1
            elif button_direction == 0:
                self.seen_position[0] -= -70
                self.player_pos[1] -= -1
            elif button_direction == 2:
                self.seen_position[1] += -70
                self.player_pos[0] += -1
            elif button_direction == 3:
                self.seen_position[1] -= -70
                self.player_pos[0] -= -1

        # Rewards here:
        self.reward = -1

        if self.done:
            self.reward = 100
        # Observations here
        info = {}

        pos_x = self.player_pos[0]
        pos_y = self.player_pos[1]

        observation = self.player_pos
        observation = np.array(observation)

        return observation, self.reward, self.done, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.done = False

        self.img = np.zeros((490, 490, 3), dtype='uint8')
        # Initial Snake and Apple position: assuming up is 0, down is 500, left is 0, right is 500.
        self.seen_position = [210, 420]
        self.apple_position = [3 * 70, 0]

        self.prev_button_direction = 1
        self.button_direction = 1

        self.player_pos = [6, 3]


        # More Stuff
        self.reward = -1

        if self.done:
            self.reward = 100
        # Observations here
        info = {}

        pos_x = self.player_pos[0]
        pos_y = self.player_pos[1]

        observation = [pos_x, pos_y]
        observation = np.array(observation)

        print(self.reward)

        return observation, info

# To Do: Code Render and Close
if __name__ == "__main__":
    env = MazeEnv()
    env.reset()

# Render

# Close