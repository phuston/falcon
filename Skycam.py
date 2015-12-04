from __future__ import division
from math import sin, cos, acos, asin, degrees, pi
import serial
from time import sleep
import numpy as np

class Skycam:
    def __init__(self, a, b, c, cam):
        self.node0, self.node1, self.node2 = self.calc_nodes(a,b,c)
        self.cam = cam
        self.direct = False
        self.pause = False
        self.save_point = 0

    def calc_nodes(a, b, c):
        ''' a opposite the origin, b is from A to C, c is along y axis
            Uppercase are angles, lowercase are lengths '''
        # Law of cosines
        numer = b**2 + c**2 - a**2
        denom = 2*b*c
        Arad = acos(numer/denom)

        # Law of sines
        Brad = asin(b*sin(Arad)/a)
        Crad = asin(c*sin(Arad)/a)

        # A = degrees(Arad)
        # B = degrees(Brad)
        # C = degrees(Crad)
        theta = .5*pi-Arad

        return (0,0, 0),  (0, c, 0), (b*cos(theta), b*sin(theta), 0)

    def load_path(self, points):
        self.path = Path.new_path(points, self.node0, self.node1, self.node2)

    def create_path(self, waypoints):
        ''' Generate a new list of points by creating a spline and then storing them in a Path object '''
        # some stuff with splines

        self.path = Path.new_path(points, self.node0, self.node1, self.node2)


    def go_path(self):
        ''' Start sending serial commands until direct mode is activated or until pause command. If paused, remember last location'''
        while (not self.direct and not self.pause):
            for i in len(self.path.diffs0[self.save_point]):
                send_command(self.path.diffs0[i], self.path.diffs1[i], self.path.diffs2)
                self.save_point = i


    def pause_path():
        ''' stop sending commands, record current point '''
        self.pause = True

    def switch_mode():
        self.direct = not self.direct

    def go_input():
        ''' translate a direct-control input into a directional vector and send appropriate commands '''

    def connect():


    def send_command():
        ''' send serial commands '''

    def dldp(self, nodePos, theta, phi):
        ''' use a directional vector and current position to calculate change in node length '''

        cam = self.cam
        deltaX = cam[0] - nodePos[0]
        deltaY = cam[1] - nodePos[1]
        deltaZ = cam[2] - nodePos[2]
        numer = deltaX*cos(theta)*cos(phi) + deltaY*sin(theta)*cos(phi) + deltaZ*sin(phi)
        denom = (deltaX**2 + deltaY**2 + deltaZ**2)**.5
        return numer/denom



class Path:
    ''' Path object stores the physical locations of the camera, and the node length changes needed to hit those spots '''
    def __init__(self, points, node0, node1, node2):
        self.points = points


        self.lens0 = [self.distance(node0, point) for point in points]
        self.lens1 = [self.distance(node1, point) for point in points]
        self.lens2 = [self.distance(node2, point) for point in points]

        self.diffs0 = self.diff_calc(self.lens0)
        self.diffs1 = self.diff_calc(self.lens1)
        self.diffs2 = self.diff_calc(self.lens2)

    @staticmethod
    def new_path(points, node0, node1, node2):
        for point in points:
            if Path.boundary(node0, node1, node2, point):
                return None

        return Path(points, node0, node1, node2)



    @staticmethod
    def boundary(node0, node1, node2, point):

        mid_AB = tuple((node0[i] + node1[i])/2 for i in xrange(3))
        mid_BC = tuple((node1[i] + node2[i])/2 for i in xrange(3))
        mid_AC = tuple((node2[i] + node0[i])/2 for i in xrange(3))

        m_A = tuple(mid - node for (mid, node) in zip(mid_BC, node0))
        m_B = tuple(mid - node for (mid, node) in zip(mid_AC, node1))
        m_C = tuple(mid - node for (mid, node) in zip(mid_AB, node2))

        # m_A = (mid_BC[0] - node0[0], mid_BC[1] - node0[1], mid_BC[2] - node0[2])
        # m_B = (mid_AC[0] - node1[0], mid_AC[1] - node1[1], mid_AC[2] - node1[2])
        # m_C = (mid_AB[0] - node2[0], mid_AB[1] - node2[1], mid_AB[2] - node2[2])

        new_0 = tuple(coord + slope*5 for (coord, slope) in zip(node0, m_A))
        new_1 = tuple(coord + slope*5 for (coord, slope) in zip(node1, m_B))
        new_2 = tuple(coord + slope*5 for (coord, slope) in zip(node2, m_C))

        if point[2] < 0 or point[2] > 60:
            print 'Height of path out of bounds'
            return True

        elif point[0] < 0:
            print "Path out of bounds of line AB"
            return True

        elif point[1] < (new_2[1]*point[0]/new_2[0]):
            print "Path out of bounds of line AC"
            return True

        elif point[1] > ((new_2[1] - new_1[1])/(new_2[0])*point[0] + new_1[1]):
            print "Path out of bounds of line BC"
            return True

        else:
            return False

    def distance(self, A, B):
        ''' Return length of wire from one position tuple to another '''

        dx = A[0] - B[0]
        dy = A[1] - B[1]
        dz = A[2] - B[2]
        return (dx**2 + dy**2 + dz**2)**.5

    def diff_calc(self, lens):
        ''' Return differences between subsequent spool lengths * 100 '''
        return [int(100*(lens[ind+1] - lens[ind])) for ind in xrange(len(lens)-1)]


newPath = Path.new_path([(.5, .5, .5), (.7, .7, .7), (20, .2, .2)], (0, 0, 0), (0, 20, 0), (40, 40, 0))
print newPath