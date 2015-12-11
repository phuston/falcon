from __future__ import division
import numpy as np
from scipy.interpolate import UnivariateSpline, splrep, splev, splprep
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def distance(posA, posB):
    dx = posA[0] - posB[0]
    dy = posA[1] - posB[1]
    dz = posA[2] - posB[2]
    return (dx**2 + dy**2 + dz**2)**.5

def binarySearch(ustart, s, dl):
    x, y, z = splev(ustart, s)
    point = (x, y, z)

    tol = .01
    ui = ustart
    uf = 1
    um = (ui + uf)/2
    xm, ym, zm = splev(um, s)
    xf, yf, zm = splev(uf, s)

    while True:
        # xi, yi = splev(ui, s)
        # xf, yf = splev(uf, s)
        xm, ym, zm= splev(um, s)
        tpoint = (xm, ym, zm)
        # print um, distance(point, tpoint)

        if distance(point, tpoint)>(dl*(1+tol)):
            uf, um = um, (um+ui)/2

        elif distance(point, tpoint)<(dl*(1-tol)):
            ui, um = um, (um+uf)/2

        else:
            return um

def splineLen(s):
    ts = np.linspace(0, 1, 1000)
    totl = 0
    xs, ys, zs = splev(ts, s)
    spline = zip(xs, ys, zs)
    ipoint = spline[0]

    for point in spline:
        totl += distance(point, ipoint)
        ipoint = point

    return totl

# declare node positions
node0 = (0,0, 0)
node1 = (0, 15, 0)
node2 = (15, 0, 0)

waypoints = [(1,1, 0), (2, 5, 0), (3, 7, 0), (4, 5, 0), (5, 2, 0), (6, 12, 0), (4, 10, 0), (2, 8, 0)]
xpoints  = [point[0] for point in waypoints]
ypoints = [point[1] for point in waypoints]
zpoints = [point[2] for point in waypoints]

# spline parameters
s=2.0 # smoothness parameter
k=2 # spline order
nest=-1 # estimate of number of knots needed (-1 = maximal)

s, us = splprep([xpoints, ypoints, zpoints], s=s,k=k,nest=nest)
totl = splineLen(s)

time = 10
steps = time*100

dl = totl/steps

i = 0
u = 0
upath = [u]

print upath

while i < steps-1:
    u = binarySearch(u, s, dl)
    upath.append(u)
    print i
    i += 1

# print dl
print upath

path = [splev(u, s) for u in upath]
xpath = [point[0] for point in path]
ypath = [point[1] for point in path]
zpath = [point[2] for point in path]

print path

pathLengths = []

for i in xrange(len(path)-1):
    pathLengths.append(distance(path[i], path[i+1]))

error = pathLengths - dl
print sum(error)/len(error)
# plt.plot(pathLengths)
# plt.show()

plt.subplot(1,2,1)
plt.plot(node0[0], node0[1], 'ro')
plt.plot(node1[0], node1[1], 'go')
plt.plot(node2[0], node2[1], 'yo')
# plt.scatter(xpoints, ypoints)
plt.scatter(xpath, ypath)
plt.xlabel('x position')
plt.ylabel('y position')
plt.title('Position of nodes and camera')

node0path = [distance(node0, loc) for loc in path]
node1path = [distance(node1, loc) for loc in path]
node2path = [distance(node2, loc) for loc in path]

# plot length of wires over time
plt.subplot(1,2,2)
plt.xlabel('time')
plt.ylabel('wire length')
plt.plot(np.linspace(0,10,steps), node0path, 'r-', label='node 0', linewidth=2)
plt.plot(np.linspace(0,10,steps), node1path, 'g-', label='node 1', linewidth=2)
plt.plot(np.linspace(0,10,steps), node2path, 'y-', label='node 2', linewidth=2)
plt.legend()
plt.title('Node wire lengths vs time')
plt.show()