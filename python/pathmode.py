from __future__ import division
import numpy as np
from math import sin, cos, acos, asin, degrees, pi
from scipy.interpolate import UnivariateSpline, splrep, splev, splint
import matplotlib.pyplot as plt

def calcnodes(a, b, c):
    numer = b**2 + c**2 - a**2
    denom = 2*b*c
    Arad = acos(numer/denom)

    Brad = asin(b*sin(Arad)/a)
    Crad = asin(c*sin(Arad)/a)

    A = degrees(Arad)
    B = degrees(Brad)
    C = degrees(Crad)

    thetA = .5*pi-Crad

    return (a*cos(thetA), a*sin(thetA), 0), (0,0, 0), (0, c, 0)

# declare node positions
a = 27.125
b = 29.25
c = 28.25
node0, node1, node2 = calcnodes(a,b,c)

# node0 = (0,0, 0)
# node1 = (0, 15, 0)
# node2 = (15, 0, 0)


# points to create path along
# path = [(1,1), (2, 5), (3, 7), (4, 5), (5, 2), (6, 12)]
# t = [n*pi/20 for n in xrange(41)]
# circlePath = [(6*cos(n) + 8, 6*sin(n) + 14, 15) for n in t]
path = [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)]

xpoints  = [point[0] for point in path]
ypoints = [point[1] for point in path]

s = splrep(xpoints, ypoints)
# s = UnivariateSpline(xpoints, ypoints, s=1)
# map spline to array of x, y points
xs = np.linspace(1, 10, 100)
ys = splev(xs, s)
t = np.linspace(0, 10, 100)

# sint = splint(1, 10, s)
# print sint
# plot nodes and camera path
plt.subplot(1,2,1)
plt.plot(node0[0], node0[1], 'ro')
plt.plot(node1[0], node1[1], 'go')
plt.plot(node2[0], node2[1], 'yo')
plt.scatter(xpoints, ypoints)
plt.xlabel('x position')
plt.ylabel('y position')
plt.title('Position of nodes and camera')


def distance(posA, posB):
    ''' Return length of wire from one position tuple to another '''

    dx = posA[0] - posB[0]
    dy = posA[1] - posB[1]
    # dz = posA[2] - posB[2]
    return (dx**2 + dy**2)**.5

# cam = zip(x, ys)

node0path = [distance(node0, loc) for loc in path]
node1path = [distance(node1, loc) for loc in path]
node2path = [distance(node2, loc) for loc in path]

# plot length of wires over time
plt.subplot(1,2,2)
plt.xlabel('time')
plt.ylabel('wire length')
plt.plot(t, node0path, 'r-', label='node 0', linewidth=2)
plt.plot(t, node1path, 'g-', label='node 1', linewidth=2)
plt.plot(t, node2path, 'y-', label='node 2', linewidth=2)
plt.legend()
plt.title('Node wire lengths vs time')
plt.show()