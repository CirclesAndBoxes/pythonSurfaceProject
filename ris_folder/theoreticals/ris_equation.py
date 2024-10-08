# Scratch work to figure out the ris environment
import jupyter_client
import jupyter_core
import numpy as np
# Attempting to apply the formula given for just 2x2

# We are trying to optimize this
powerReturned = 0

# Defining some constants
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

# Returns maximum positive distances
def maxSum(n, m):
    out = (1 / (rTransmitterDistances[n][m] * rReceiverDistances[n][m]))
    return out
#def doubleSum(phiList):

# Slightly less calculation intense method of calculating the square of a magnitude of a complex:
# https://www.geeksforgeeks.org/finding-magnitude-of-a-complex-number-in-python/
def magnitude_squared(z):
    return (z.real**2 + z.imag**2)

phiList = [0.8165892,  0.96166354, 0.78221714,  0.18471748, -0.6022426,   0.0777506,
 -0.8130401,  -0.17920643,  0.19263078, 0.7356156,   0.15492606, -0.08065471,
 -0.1400515,   0.42800143,  0.7372323,   0.13771912]
# Summing together the double summation. Using 0 as a temp value of phi
crazySummation = 0
for m in range(numYCells):
    for n in range(numXCells):
        crazySummation += insideSum(n, m, PI + PI * phiList[m * numXCells + n])

maxSummation = 0
for m in range(numYCells):
    for n in range(numXCells):
        maxSummation += maxSum(n, m)

# Plug it all into the final value
powerReturned = ((powerTransmitted * gVariables * dx * dy * (wavelength**2) / (64 * (PI ** 3))) *
                 (magnitude_squared(crazySummation)))

maxPowerReturned = ((powerTransmitted * gVariables * dx * dy * (wavelength**2) / (64 * (PI ** 3))) *
                 (magnitude_squared(maxSummation)))

checker = 0
for m in range(numYCells):
    for n in range(numXCells):
        checker += abs(phiList[m * numXCells + n])

print(powerReturned)

print(maxPowerReturned)

print(magnitude_squared(maxSum(1,1)))
print(magnitude_squared(insideSum(1,1,0)))