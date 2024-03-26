# source: https://github.com/TheAILearner/Snake-Game-using-OpenCV-Python/blob/master/snake_game_using_opencv.ipynb
import numpy as np
import cv2
import random
import time
import generated_maze

# a 7 by 7 maze. 1 means wall, 0 means gap, 2 means exit
# Positions: [row][column]
# Initial position: maze[6][3]
# Final position: maze[0][3]
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


img = np.zeros((490, 490, 3), dtype='uint8')
# Initial Snake and Apple position: assuming up is 0, down is 500, left is 0, right is 500.
seen_position = [210, 420]
apple_position = [3 * 70, 0]

prev_button_direction = 1
button_direction = 1

player_pos = [6, 3]

while True:
    cv2.imshow('a', img)
    cv2.waitKey(1)
    img = np.zeros((490, 490, 3), dtype='uint8')
    # Display Apple
    cv2.rectangle(img, (apple_position[0], apple_position[1]), (apple_position[0] + 70, apple_position[1] + 70),
                  (0, 0, 255), 3)
    # Display Snake

    cv2.rectangle(img, (seen_position[0], seen_position[1]), (seen_position[0] + 70, seen_position[1] + 70), (0, 255, 0), 3)

    # Display Maze:

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                cv2.rectangle(img, (j * 70, i * 70), (j * 70 + 70, i * 70 + 70),
                          (255, 255, 255), 3)


    # Takes step after fixed time
    t_end = time.time() + 0.05
    k = -1
    k = cv2.waitKey(1)
    while time.time() < t_end:
        if k == -1:
            k = cv2.waitKey(1)
        else:
            continue

    # 0-Left, 1-Right, 3-Up, 2-Down, q-Break
    # a-Left, d-Right, w-Up, s-Down

    if k == ord('a'):
        button_direction = 0
    elif k == ord('d'):
        button_direction = 1
    elif k == ord('w'):
        button_direction = 3
    elif k == ord('s'):
        button_direction = 2
    elif k == ord('q'):
        break
    else:
        button_direction = -1

    # Change the position based on the button direction
    if button_direction == 1:
        seen_position[0] += 70
        player_pos[1] += 1
    elif button_direction == 0:
        seen_position[0] -= 70
        player_pos[1] -= 1
    elif button_direction == 2:
        seen_position[1] += 70
        player_pos[0] += 1
    elif button_direction == 3:
        seen_position[1] -= 70
        player_pos[0] -= 1

    # End game when reaching end
    if seen_position == apple_position:
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = np.zeros((490, 490, 3), dtype='uint8')
        cv2.putText(img, 'You win!', (140, 250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('a', img)
        cv2.waitKey(0)
        break


    if collision_with_boundaries(seen_position) == 1:
        if button_direction == 1:
            seen_position[0] += -70
            player_pos[1] += -1
        elif button_direction == 0:
            seen_position[0] -= -70
            player_pos[1] -= -1
        elif button_direction == 2:
            seen_position[1] += -70
            player_pos[0] += -1
        elif button_direction == 3:
            seen_position[1] -= -70
            player_pos[0] -= -1
    elif collision_with_maze(player_pos):
        if button_direction == 1:
            seen_position[0] += -70
            player_pos[1] += -1
        elif button_direction == 0:
            seen_position[0] -= -70
            player_pos[1] -= -1
        elif button_direction == 2:
            seen_position[1] += -70
            player_pos[0] += -1
        elif button_direction == 3:
            seen_position[1] -= -70
            player_pos[0] -= -1

cv2.destroyAllWindows()