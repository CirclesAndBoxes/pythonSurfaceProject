import gymnasium as gym
import numpy as np
from gymnasium import spaces
# PPO Variables
resetCount = 0


# Equation variables
powerTransmitted = 1e16
gVariables = 1
dx = 1
dy = 1
# meters? This is for about 3 GHz
wavelength = 0.1
PI = 3.14159265358979323846
E = 2.7182818284590452353602874713527
# Written as M,N. i think we assume they're even
numXCells, numYCells = 4, 4
transmitterPosition = (100, 200, 300)
receiverPosition = (-100, -210, 300)

# cell[x][y] = (1, 2, 0) or something
def cellPositions(tPos, rPos):
    out = []
    for x in range(numXCells):
        out.append([])
        for y in range(numYCells):
            coordX = (1 - (numXCells / 2) + x) * dx
            coordY = (1 - (numYCells / 2) + y) * dy
            out[x].append((coordX, coordY, 0))
    return out

cellPos = cellPositions(transmitterPosition, receiverPosition)


# Create and populate r values:
#region
rTransmitterDistances = []
rReceiverDistances = []
for x in range(numXCells):
    rTransmitterDistances.append([])
    rReceiverDistances.append([])
    for y in range(numYCells):
        receiveDistX = cellPos[x][y][0] - receiverPosition[0]
        receiveDistY = cellPos[x][y][1] - receiverPosition[1]
        receiveDistZ = cellPos[x][y][2] - receiverPosition[2]
        rReceiverDistances[x].append(np.sqrt((receiveDistX ** 2) + (receiveDistY ** 2) + (receiveDistZ ** 2)))
        transmitDistX = cellPos[x][y][0] - transmitterPosition[0]
        transmitDistY = cellPos[x][y][1] - transmitterPosition[1]
        transmitDistZ = cellPos[x][y][2] - transmitterPosition[2]
        rTransmitterDistances[x].append(np.sqrt((transmitDistX ** 2) + (transmitDistY ** 2) + (transmitDistZ ** 2)))
#endregion

# This is the one that can be modified for each cell. It looks like a partial T. phi is a variable that can change
##      gamma = A e^(j Phi)
def gamma(phi):
    return 1 * E ** (1J * phi)

# Creating the inside of the summation notation
def insideSum(n, m, phi):
    out = (1 * gamma(phi) / (rTransmitterDistances[n][m] * rReceiverDistances[n][m]))
    out = out * E ** (- 1J * 2 * PI * (rTransmitterDistances[n][m] + rReceiverDistances[n][m]) / wavelength)
    return out

def maxSum(n, m):
    out = (1 / (rTransmitterDistances[n][m] * rReceiverDistances[n][m]))
    return out

# Slightly less calculation intense method of calculating the square of a magnitude of a complex:
# https://www.geeksforgeeks.org/finding-magnitude-of-a-complex-number-in-python/
def magnitude_squared(z):
    return (z.real**2 + z.imag**2)

# Summing together the double summation. Using 0 as a temp value of phi
crazySummation = 0
for m in range(numYCells):
    for n in range(numXCells):
        crazySummation += insideSum(n, m, 0)

maxSummation = 0
for m in range(numYCells):
    for n in range(numXCells):
        maxSummation += maxSum(n, m)

# Plug it all into the final value
powerReturned = ((powerTransmitted * gVariables * dx * dy * (wavelength**2) / (64 * (PI ** 3))) *
                 (magnitude_squared(crazySummation)))

maxPowerReturned = ((powerTransmitted * gVariables * dx * dy * (wavelength**2) / (64 * (PI ** 3))) *
                 (magnitude_squared(maxSummation)))

def givePower(phiList):
    crazySummation = 0
    for m in range(numYCells):
        for n in range(numXCells):
            # note: changed the value of phiList to account for the change in spaces
            crazySummation += insideSum(n, m, phiList[m * numXCells + n] * PI + PI)

    # Plug it all into the final value
    return ((powerTransmitted * gVariables * dx * dy * (wavelength ** 2) / (64 * (PI ** 3))) *
                     (magnitude_squared(crazySummation)))

def giveMaxPower():
    maxSummation = 0
    for m in range(numYCells):
        for n in range(numXCells):
            maxSummation += maxSum(n, m)

    return ((powerTransmitted * gVariables * dx * dy * (wavelength ** 2) / (64 * (PI ** 3))) *
                        (magnitude_squared(maxSummation)))

class RisEnvConst(gym.Env):
    """Custom Environment that follows gym interface."""
    # Idk what this is for
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super(RisEnvConst, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Trying to use continuous space actions:
        #   https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html#tips-and-tricks-when-creating-a-custom-environment
        #   "Action space normalized and has interval range of 2. Gaussian distribution?"
        # Trying shape is 16 because 4 x 4 sized box. Generates a list!
        self.action_space = spaces.Box(low=-1, high=1, shape=(16,), dtype="float32")
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-500, high=500,
                                            shape=(6,), dtype=np.float32)



    def step(self, action):
        self.num_actions += 1
        if self.num_actions >= 10:
            self.done = True

        # Modified reward so we get at least half strength?
        reward = 10 * (float(givePower(action)) / float(giveMaxPower())) - 5

        # Change observation to be the location of the transmitter and receiver
        #
        observation = np.array([transmitterPosition[0], transmitterPosition[1], transmitterPosition[2],receiverPosition[0], receiverPosition[1], receiverPosition[2]],
                               dtype=np.float32)
        self.reward = reward
        terminated = self.done
        truncated = False
        info = {}

        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        #global resetCount
        #global transmitterPosition
        #global receiverPosition
        #resetCount += 1
        #if resetCount % 100 == 1:
        #    print(resetCount, transmitterPosition, receiverPosition)

        # transmitterPosition = np.random.rand(3) * 200 - 100
        # receiverPosition = np.random.rand(3) * 200 - 100

        if 'self.reward' in globals():
            print(self.reward)

        self.done = False
        self.num_actions = 0

        self.observation = np.array([transmitterPosition[0], transmitterPosition[1], transmitterPosition[2],receiverPosition[0], receiverPosition[1], receiverPosition[2]],
                                    dtype=np.float32)
        observation = self.observation
        info = {}
        return observation, info

    # def render(self):
    #     ...
    #
    # def close(self):
    #     ...