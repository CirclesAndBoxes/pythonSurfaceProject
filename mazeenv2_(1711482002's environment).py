import gymnasium as gym
import numpy as np
from gymnasium import spaces
import cv2
import random
import time
from collections import deque
import generated_maze


maze = generated_maze.generate_maze(4, 4)
maze[0][3] = 2


def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_position, score


def collision_with_boundaries(snake_head):
    if snake_head[0] >= 490 or snake_head[0] < 0 or snake_head[1] >= 490 or snake_head[1] < 0:
        return 1
    else:
        return 0


# Did it collide into the maze or itself?
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


def been_here_last_two(position, last_position):
    if position[0] == last_position[0] and position[1] == last_position[1]:
        return True
    else:
        return False


class MazeEnv2_2(gym.Env):
    """Custom Environment that follows gym interface."""

    # metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super(MazeEnv2_2, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works) Shape must be exact:
        self.observation_space = spaces.Box(low=-20, high=1001,
                                            shape=(109,), dtype=np.int32)

    def step(self, action):
        cv2.imshow('a', self.img)
        cv2.waitKey(1)
        self.img = np.zeros((490, 490, 3), dtype='uint8')
        # Display Apple
        cv2.rectangle(self.img, (self.apple_position[0], self.apple_position[1]), (self.apple_position[0] + 70, self.apple_position[1] + 70),
                      (0, 0, 255), 3)
        # Display player

        cv2.rectangle(self.img, (self.seen_position[0], self.seen_position[1]), (self.seen_position[0] + 70, self.seen_position[1] + 70),
                      (0, 255, 0), 3)

        # Magic: takes step after fixed time code?
        t_end = time.time() + 0.001
        k = -1
        while time.time() < t_end:
            if k == -1:
                k = cv2.waitKey(1)
            else:
                continue


        # Display Maze:

        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 1:
                    cv2.rectangle(self.img, (j * 70, i * 70), (j * 70 + 70, i * 70 + 70),
                                  (255, 255, 255), 3)




        # Action
        button_direction = action

        # Change the position based on the button direction
        if button_direction == 1:
            self.seen_position[0] += 70
            self.player_pos[1] += 1
            self.last_direction = 1
        elif button_direction == 0:
            self.seen_position[0] -= 70
            self.player_pos[1] -= 1
            self.last_direction = 0
        elif button_direction == 2:
            self.seen_position[1] += 70
            self.player_pos[0] += 1
            self.last_direction = 2
        elif button_direction == 3:
            self.seen_position[1] -= 70
            self.player_pos[0] -= 1
            self.last_direction = 3

        # End game when reaching ends
        if self.seen_position == self.apple_position:
            font = cv2.FONT_HERSHEY_SIMPLEX
            self.img = np.zeros((490, 490, 3), dtype='uint8')
            cv2.putText(self.img, 'You win!', (140, 250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('a', self.img)
            self.done = True

        # Also ending game if too many steps are taken
        if self.steps_left < 0:
            self.reward = -100
            self.done = True


        self.reward = -1
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
            self.reward = -5
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
            self.reward = -5

        # Checks if was in same place 2 steps ago:
        if been_here_last_two(self.player_pos, self.last_two_pos):
            self.reward += -1
            was_here = 1
        else:
            was_here = 0



        # Rewards here:

        # Punish for not ending/bumping into wall already above.
        if self.done and self.steps_left >= 0:
            self.reward = 300
        elif self.done:
            self.reward = -100



        # Observations here
        info = {}

        # Making sure up/down/left/right actually align to the x and y axies
        pos_x = self.player_pos[1]
        pos_y = self.player_pos[0]

        # 1 = block or edge, 0 = empty
        if pos_x == 0:
            left_side = 1
        elif maze[pos_y][pos_x - 1] == 1:
            left_side = 1
        else:
            left_side = 0

        if pos_x == 6:
            right_side = 1
        elif maze[pos_y][pos_x + 1] == 1:
            right_side = 1
        else:
            right_side = 0

        if pos_y == 0:
            up_side = 1
        elif maze[pos_y - 1][pos_x] == 1:
            up_side = 1
        else:
            up_side = 0

        if pos_y == 6:
            down_side = 1
        elif maze[pos_y + 1][pos_x] == 1:
            down_side = 1
        else:
            down_side = 0

        two_ago_x, two_ago_y = self.last_two_pos[0], self.last_two_pos[1]
        last_direction = self.last_direction
        steps_left = self.steps_left

        # Punishment if returning to previous position
        if self.been_maze[pos_y][pos_x] > 0:
            self.reward -= 1

        # Remember previous steps -- WARNING SOMEHOW GENERATES NEW BLOCKS IDK HOW BUT HOPEFULLY THIS CHANGES STUFF
        self.been_maze[pos_y][pos_x] += 3


        # Adding left/right/etc. sides helps teach the robot learn faster
        # Maybe try without left/right/etc., see if it takes longer

        # Include last step
        observation = [pos_x, pos_y, left_side, right_side, up_side, down_side, was_here, two_ago_x, two_ago_y,
                       last_direction, steps_left]
        # Adds another 49 observations
        for row in maze:
            for element in row:
                observation.append(element)
        # Then adds another 49 observations
        for row in self.been_maze:
            for element in row:
                observation.append(element)

        observation = np.array(observation)

        self.last_two_pos = self.last_pos
        self.last_pos = self.player_pos
        self.last_direction = action
        self.steps_left -= 1

        # check this line
        return observation, self.reward, self.done, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        global maze
        # Issue is that maze is currently not being sent out to the outside
        # Builds the maze in front
        maze = generated_maze.generate_maze(4, 4)
        maze[0][3] = 2

        # Resets last two positions
        self.last_pos = [6, 3]
        self.last_two_pos = [6, 3]

        # Resets the number of steps left
        self.steps_left = 1000

        #Next line is done twice
        self.done = False

        self.img = np.zeros((490, 490, 3), dtype='uint8')
        # Initial Snake and Apple position: assuming up is 0, down is 500, left is 0, right is 500.
        self.seen_position = [210, 420]
        self.apple_position = [3 * 70, 0]

        self.prev_button_direction = 1
        self.button_direction = 1
        self.last_direction = -1

        self.player_pos = [6, 3]

        self.done = False

        # More Stuff
        self.reward = 0

        # Maze of where the agent has been
        self.been_maze = maze

        if self.done:
            self.reward = 300
        # Observations here
        info = {}

        # Making sure up/down/left/right actually align to the x and y axies
        pos_x = self.player_pos[1]
        pos_y = self.player_pos[0]

        # 1 = block or edge, 0 = empty
        if pos_x == 0:
            left_side = 1
        elif maze[pos_y][pos_x - 1] == 1:
            left_side = 1
        else:
            left_side = 0

        if pos_x == 6:
            right_side = 1
        elif maze[pos_y][pos_x + 1] == 1:
            right_side = 1
        else:
            right_side = 0

        if pos_y == 0:
            up_side = 1
        elif maze[pos_y - 1][pos_x] == 1:
            up_side = 1
        else:
            up_side = 0

        if pos_y == 6:
            down_side = 1
        elif maze[pos_y + 1][pos_x] == 1:
            down_side = 1
        else:
            down_side = 0


        # Some new variables
        was_here = 0

        two_ago_x, two_ago_y = self.last_two_pos[0], self.last_two_pos[1]

        last_direction = self.last_direction
        steps_left = self.steps_left
        # I moved the observation down.

        # An Unneeded line, but one that lets us know the length it takes on average
        print(self.reward)



        observation = [pos_x, pos_y, left_side, right_side, up_side, down_side, was_here, two_ago_x, two_ago_y,
                       last_direction, steps_left]
        # Adds another 49 observations
        for row in maze:
            for element in row:
                observation.append(element)
        # Then adds another 49 observations
        for row in self.been_maze:
            for element in row:
                observation.append(element)

        observation = np.array(observation)

        return observation, info

# To Do: Code Render and Close


# Render

# Close