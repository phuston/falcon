from __future__ import division
from math import sin, cos, acos, asin, degrees, pi
import serial
from time import sleep
import numpy as np

raw_input("Press ENTER to begin Serial connection.")
serE = serial.Serial('/dev/rfcomm0', 9600, timeout=50)
serNW = serial.Serial('/dev/rfcomm1', 9600, timeout=50)
# serSW = serial.Serial('/dev/ttyACM3', 9600, timeout=50)

print "Hacking into the mainframe... "
sleep(.5)
raw_input("Press ENTER to begin. ")

def distance(posA, posB):
    ''' Return length of wire from one position tuple to another '''

    dx = posA[0] - posB[0]
    dy = posA[1] - posB[1]
    dz = posA[2] - posB[2]
    return (dx**2 + dy**2 + dz**2)**.5

def dldp(cameraPos, nodePos, theta, phi):
    deltaX = cameraPos[0] - nodePos[0]
    deltaY = cameraPos[1] - nodePos[1]
    deltaZ = cameraPos[2] - nodePos[2]
    numer = deltaX*cos(theta)*cos(phi) + deltaY*sin(theta)*cos(phi) + deltaZ*sin(phi)
    denom = (deltaX**2 + deltaY**2 + deltaZ**2)**.5
    return numer/denom

def calcnodes(a, b, c):
    ''' b is your origin, c is along y axis, a is opposite '''

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

def calcsend(camera, theta, phi, posA, posB, posC):
    ''' For directional control '''

    Eval = int(100*dldp(camera, posA, theta, phi))
    SWval = int(100*dldp(camera, posB, theta, phi))
    NWval = int(100*dldp(camera, posC, theta, phi))

    print Eval, NWval, SWval
    print camera

    serE.write(str(Eval) + 'g')
    # serSW.write(str(SWval) + 'g')
    serNW.write(str(NWval) + 'g')

def diffcalc(path, node0, node1, node2):
    ''' given array of coordinates for camera to hit
        generate an array of lengths for each node '''

    node0path = [distance(node0, loc) for loc in path]
    node1path = [distance(node1, loc) for loc in path]
    node2path = [distance(node2, loc) for loc in path]

    node0diff = [int(100*(node0path[ind+1] - node0path[ind])) for ind in xrange(len(node0path)-1)]
    node1diff = [int(100*(node1path[ind+1] - node1path[ind])) for ind in xrange(len(node1path)-1)]
    node2diff = [int(100*(node2path[ind+1] - node2path[ind])) for ind in xrange(len(node2path)-1)]


    if (sum(node0diff) + node0path[0]) == node0path[-1]:
        print 'Math Checks out'

    return node0diff, node1diff, node2diff

a = 75.75
b = 53.25
c = 89.5
posA, posB, posC = calcnodes(a,b,c)
print posA, posB, posC
camera = (7, 4.5, 18.5)

''' Move up 10 inches '''
path3 = [(camera[0], camera[1], camera[2] + .2*n) for n in xrange(50)]

''' Move north and up 16 inches '''
path1 = [(camera[0], camera[1] + .2*n, camera[2] - .2*n) for n in xrange(22)]
camera = (7, 20.5, 2.5)

''' Go in a circle of radius 12 inches '''
thetas = [((pi) + (m*pi/50)) for m in xrange(101)]
path2 = [(camera[0] + 6 + 6*cos(theta), camera[1] + 6*sin(theta), camera[2]) for theta in thetas]

path4 = [(camera[0] + .2*n, camera[1], camera[2] + .2*n) for n in xrange(80)]

path = path2
node0diff, node1diff, node2diff = diffcalc(path, posA, posB, posC)

print node0diff
print node1diff
print node2diff

for i in xrange(len(node0diff)):
    serE.write(str(node0diff[i]) + 'g')
    serNW.write(str(node2diff[i]) + 'g')
    # serSW.write(str(node1diff[i]) + 'g')
    sleep(.1)

# node0diff, node1diff, node2diff = diffcalc(path4, posA, posB, posC)

# for i in xrange(len(node0diff)):
#     serE.write(str(node0diff[i]) + 'g')
#     serNW.write(str(node2diff[i]) + 'g')
#     serSW.write(str(node1diff[i]) + 'g')
#     # sleep(.5)






while True:
    cmd = raw_input("")
    print camera
    if cmd is 'x':
        break

    if cmd is 'w':
        theta = pi/2
        phi = 0
        calcsend(camera, theta, phi, posA, posB, posC)
        camera = (camera[0], camera[1]+1, camera[2])

    if cmd is 'a':
        theta = pi
        phi = 0
        calcsend(camera, theta, phi, posA, posB, posC)
        camera = (camera[0]-1, camera[1], camera[2])

    if cmd is 's':
        theta = 3*pi/2
        phi = 0
        calcsend(camera, theta, phi, posA, posB, posC)
        camera = (camera[0], camera[1]-1, camera[2])

    if cmd is 'd':
        theta = 0
        phi = 0
        calcsend(camera, theta, phi, posA, posB, posC)
        camera = (camera[0]+1, camera[1], camera[2])

    if cmd is 'h':
        theta = 0
        phi = 3*pi/2
        calcsend(camera, theta, phi, posA, posB, posC)
        camera = (camera[0], camera[1], camera[2]-1)

    if cmd is 'l':
        theta = 0
        phi = pi/2
        calcsend(camera, theta, phi, posA, posB, posC)
        camera = (camera[0], camera[1], camera[2]+1)
