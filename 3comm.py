from __future__ import division
from math import sin, cos, acos, asin, degrees, pi
import serial
from time import sleep
import numpy as np

raw_input("Press ENTER to begin Serial connection.")
serE = serial.Serial('/dev/ttyACM0',9600,timeout=50)
serNW = serial.Serial('/dev/ttyACM1',9600,timeout=50)
serSW = serial.Serial('/dev/ttyACM2',9600,timeout=50)

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
    Eval = int(100*dldp(camera, posA, theta, phi))
    SWval = int(100*dldp(camera, posB, theta, phi))
    NWval = int(100*dldp(camera, posC, theta, phi))

    print Eval, NWval, SWval
    print camera

    serE.write(str(Eval))
    serSW.write(str(SWval))
    serNW.write(str(NWval))

def diffcalc(path, node0, node1, node2):
    node0path = [distance(node0, loc) for loc in path]
    node1path = [distance(node1, loc) for loc in path]
    node2path = [distance(node2, loc) for loc in path]

    node0diff = [(node0path[ind+1] - node0path[ind]) for ind in xrange(len(node0path)-1)]
    node1diff = [(node1path[ind+1] - node1path[ind]) for ind in xrange(len(node1path)-1)]
    node2diff = [(node2path[ind+1] - node2path[ind]) for ind in xrange(len(node2path)-1)]

    return node0diff, node1diff, node2diff

a = 27.125
b = 29.25
c = 28.25
posA, posB, posC = calcnodes(a,b,c)
camera = (8.75, 11.0, 24.5)


t = [n*pi/20 for n in xrange(41)]
circlePath = [(6*cos(n) + 8, 6*sin(n) + 14, 15) for n in t]
diff0, diff1, diff2 = diffcalc(circlePath, posA, posB, posC)

for i in xrange(5):
    theta = 0
    phi = 3*pi/2
    calcsend(camera, theta, phi, posA, posB, posC)
    camera = (camera[0], camera[1], camera[2] - 1)

for i in xrange(len(diff0)):
    phi = 0
    serE.write(str(diff0))
    serSW.write(str(diff1))
    serNW.write(str(diff2))


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
