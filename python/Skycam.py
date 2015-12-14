from __future__ import division
from math import sin, cos, acos, asin, degrees, pi
import serial
from time import sleep
import numpy as np
from scipy.interpolate import splprep, splev, splrep

class Skycam:
    ''' Represents entire 3-node and camera system. Contains method to calculate
        and initialize paths, and control the camera.
    '''

    def __init__(self, a, b, c, zB, zC, cam):
        ''' Intialize new Skycam with calculated node positions, camera position,
            in path-controlled mode.

            Inputs:
                a: (float) length of side a
                b: (float) length of side b
                c: (float) length of side c
                zB: (float) height of point B
                zC: (float) height of point C
                cam: (tuple of floats) initial position of camera
        '''
        self.node0, self.node1, self.node2 = self.calc_nodes(a, b, c, zB, zC)
        self.cam = cam
        self.direct = False
        self.pause = False
        self.save_point = 0

    def calc_nodes(self, a, b, c, zB, zC):
        ''' Calculate the positions of Skycam nodes based on node distance measurements.
            A is the origin, B is along the y-axis, C is the remaining point.
            Sides are opposite their respective points:
                a is BC, b is AC, c is AB

            Inputs:
                a: (float) length of side a
                b: (float) length of side b
                c: (float) length of side c

            Returns:
                (tuple of floats) coordinates of node0, node1, node2
        '''
        # Project lengths into xy plane
        a_eff = ((zC-zB)**2 + c**2)**.5
        b_eff = (zC**2 + b**2)**.5
        c_eff = (zB**2 + c**2)**.5


        # Law of cosines
        numer = b_eff**2 + c_eff**2 - a_eff**2
        denom = 2*b_eff*c_eff
        Arad = acos(numer/denom)

        # Law of sines
        Brad = asin(b*sin(Arad)/a)
        Crad = asin(c*sin(Arad)/a)

        theta = .5*pi-Arad

        return (0,0, 0),  (0, c, zB), (b*cos(theta), b*sin(theta), zC)

    def load_path(self, points):
        ''' Initialize a new Path object and assign as attribute of Skycam.

            Inputs:
                points: (list of tuples of floats) specific camera positions for
                        any given time.
        '''
        self.path = Path.new_path(points, self.node0, self.node1, self.node2)

    def create_path(self, waypoints, time):
        ''' Generate a new list of points by creating a spline and then storing them in a Path object '''

        xpoints = [point[0] for point in waypoints]
        ypoints = [point[1] for point in waypoints]
        zpoints = [point[2] for point in waypoints]

        # spline parameters
        s = 2.0 # smoothness
        k = 1 # spline order
        nest = -1 # estimate of knots needed

        # create spline and calculate length
        s, us = splprep([xpoints, ypoints, zpoints], s=s, k=k, nest=nest)
        totl = self.splineLen(s)

        steps = time*100
        dl = totl/steps

        i = 0
        u = 0
        upath = [u]

        while i < steps-1:
            u = self.binary_search(u, s, dl) # optionally pass tolerance
            upath.append(u)
            print i
            i += 1

        path = [splev(u, s) for u in upath]
        path_lens = []

        for i in xrange(len(path) - 1):
            path_lens.append(distance(path[i], path[i+1]))

        error = [ele - dl for ele in path_lens]
        print 'Error is: ', sum(error)/len(error)

        self.path = Path.new_path(path, self.node0, self.node1, self.node2)


    def go_path(self):
        ''' Start sending serial commands until direct mode is activated or until pause command. If paused, remember last location'''
        while (not self.direct and not self.pause):
            for i in len(self.path.diffs0[self.save_point:]):
                self.send_command(self.path.diffs0[i+self.save_point], self.path.diffs1[i+self.save_point], self.path.diffs2+self.save_point)
                self.save_point = i


    def pause_path(self):
        ''' Pause the  '''
        self.pause = True

    def switch_mode(self):
        ''' Switch from path control to joystick control '''
        self.direct = not self.direct

    def go_input(self):
        ''' translate a direct-control input into a directional vector and send appropriate commands '''
        pass

    def connect(self, baud=57600):
        ''' Run bash script to connect to Arduinos through proper serial ports '''

        # Connect to proper serial ports
        serA = serial.Serial('/dev/rfcomm0', baud, timeout=50)
        serB = serial.Serial('/dev/rfcomm1', baud, timeout=50)
        serC = serial.Serial('/dev/rfcomm2', baud, timeout=50)


    def send_command(self, diff0, diff1, diff2):
        ''' send serial commands '''

        serA.write(str(diff0 + 'g'))
        serB.write(str(diff1 + 'g'))
        serC.write(str(diff2 + 'g'))

        #TODO: Mess around with this value
        sleep(.1)

        pass

    def dldp(self, nodePos, theta, phi):
        ''' use a directional vector and current position to calculate change in node length '''

        cam = self.cam
        deltaX = cam[0] - nodePos[0]
        deltaY = cam[1] - nodePos[1]
        deltaZ = cam[2] - nodePos[2]
        numer = deltaX*cos(theta)*cos(phi) + deltaY*sin(theta)*cos(phi) + deltaZ*sin(phi)
        denom = (deltaX**2 + deltaY**2 + deltaZ**2)**.5
        return numer/denom

    def binary_search(self, ustart, s, dl, tol=.01):
        ''' Perform a binary search to find parametrized location of point '''

        point = splev(ustart, s)

        ui = ustart
        uf = 1
        um = (ui + uf)/2

        xm, ym, zm = splev(um, s)
        xf, yf, zf = splev(uf, s)

        while True:
            tpoint = splev(um, s)

            if distance(point, tpoint)>(dl*(1+tol)):
                uf, um = um, (um+ui)/2

            elif distance(point, tpoint)<(dl*(1-tol)):
                ui, um = um, (um+uf)/2

            else:
                return um

    def splineLen(self, s):
        ts = np.linspace(0, 1, 1000)
        xs, ys, zs = splev(ts, s)
        spline = zip(xs, ys, zs)

        ipoint = spline[0]
        totl = 0

        for point in spline:
            totl += distance(point, ipoint)
            ipoint = point

        return totl

    def tighten_A(self):
        while True:
            input = raw_input('')
            if input == ' ':
                serA.write('30g')
            elif input == 's':
                return

    def tighten_B(self):
        while True:
            input = raw_input('')
            if input == ' ':
                serB.write('30g')
            elif input == 's':
                return

    def tighten_C(self):
        while True:
            input = raw_input('')
            if input == ' ':
                serC.write('30g')
            elif input == 's':
                return

class Path:
    ''' Path object stores the physical locations of the camera, and the node length changes needed to hit those spots '''
    def __init__(self, points, node0, node1, node2):
        self.points = points

        self.lens0 = [distance(node0, point) for point in points]
        self.lens1 = [distance(node1, point) for point in points]
        self.lens2 = [distance(node2, point) for point in points]

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
    def boundary(node0, node1, node2, point, offset=6, hbound=60):

        mid_AB = tuple((node0[i] + node1[i])/2 for i in xrange(3))
        mid_BC = tuple((node1[i] + node2[i])/2 for i in xrange(3))
        mid_AC = tuple((node2[i] + node0[i])/2 for i in xrange(3))

        m_A = tuple((mid - node)/distance(mid_BC, node0) for (mid, node) in zip(mid_BC, node0))
        m_B = tuple((mid - node)/distance(mid_AC, node1) for (mid, node) in zip(mid_AC, node1))
        m_C = tuple((mid - node)/distance(mid_AB, node2) for (mid, node) in zip(mid_AB, node2))

        new_0 = tuple(coord + slope*offset for (coord, slope) in zip(node0, m_A))
        new_1 = tuple(coord + slope*offset for (coord, slope) in zip(node1, m_B))
        new_2 = tuple(coord + slope*offset for (coord, slope) in zip(node2, m_C))

        if point[2] < 0 or point[2] > hbound:
            print 'Height of path out of bounds'
            return True

        elif point[0] < 0:
            print "Path out of bounds of line AB"
            return True

        elif point[1] < (new_2[1]*point[0]/new_2[0]):
            print "Path out of bounds of line AC"
            return True

        elif point[1] > (((new_2[1] - new_1[1])/new_2[0])*point[0] + new_1[1]):
            print ((new_2[1] - new_1[1])/new_2[0])*point[0] + new_1[1] - point[1]
            print "Path out of bounds of line BC"
            return True

        else:
            return False

    def diff_calc(self, lens):
        ''' Return differences between subsequent spool lengths * 100 '''
        return [int(100*(lens[ind+1] - lens[ind])) for ind in xrange(len(lens)-1)]

def distance(A, B):
    ''' Return length of wire from one position tuple to another '''

    dx = A[0] - B[0]
    dy = A[1] - B[1]
    dz = A[2] - B[2]
    return (dx**2 + dy**2 + dz**2)**.5
