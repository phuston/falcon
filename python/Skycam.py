from __future__ import division
from math import sin, cos, acos, asin, degrees, pi
import serial
from time import sleep
import numpy as np
from scipy.interpolate import splprep, splev, splrep

class Skycam:
    ''' Represents entire 3-node and camera system. Contains methods to calculate
        and initialize paths, control the camera, connect and send serial commands.
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
        ''' Create a new path based on predetermined points.

            Inputs:
                points: (list of tuples of floats) specific camera positions for
                        any given time.

            Returns:
                Initializes new Path in Skycam's path attribute
        '''
        self.path = Path.new_path(points, self.node0, self.node1, self.node2)

    def create_path(self, waypoints, steps):
        ''' Generate a new list of points based on waypoints.

            Inputs:
                waypoints: (list of tuples of floats): points the path should
                            bring the camera to
                steps: (int) number of steps in which to complete the path

            Returns:
                Calls load_path method on list of generated spline points
        '''

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

        dl = totl/steps

        if dl > 1:
            print "dl greater than 1!"

        i = 0
        u = 0
        upath = [u]

        # Divide path into equidistant lengths
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

        self.load_path(path)
        # self.path = Path.new_path(path, self.node0, self.node1, self.node2)


    def go_path(self, start):
        '''Send appropriate movement commands for loaded path.

            Input:
                start: (int) index of path at which to begin sending commands
        '''
        #TODO: Implement save point
        while (not self.direct and not self.pause):
            for i in xrange(len(self.path.diffs0) - start):
                self.send_command(self.path.diffs0[i + start], self.path.diffs1[i + start], self.path.diffs2[i + start])
                # raw_input('')
                self.save_point = i
            break


    # def pause_path(self):
    #     ''' Pause path traversal.'''
    #     self.pause = True

    # def switch_mode(self):
    #     ''' Switch from path control to joystick control '''
    #     self.direct = not self.direct

    # def go_input(self):
    #     ''' Translate a direct-control input into a directional vector and send appropriate commands '''
    #     pass

    def connect(self, baud=57600):
        ''' Connect to proper serial ports for Bluetooth communication.

            Inputs:
                baud: (int) baud rate at which to connect

            Returns:
                Print confirmation of connection
         '''

        # Connect to proper serial ports
        self.serA = serial.Serial('/dev/rfcomm0', baud, timeout=50)
        self.serB = serial.Serial('/dev/rfcomm1', baud, timeout=50)
        self.serC = serial.Serial('/dev/rfcomm2', baud, timeout=50)
        print 'Hacking the mainframe...'
        sleep(8)
        print 'Mainframe hacked'


    def send_command(self, diff0, diff1, diff2):
        '''Send proper commands to all three serial ports.

            Inputs:
                diff0: (float) node length difference for node 0
                diff1: (float) node length difference for node 1
                diff2: (float) node length difference for node 2
         '''
        print diff0, diff1, diff2

        self.serA.write(str(diff0) + 'g')
        self.serB.write(str(diff1) + 'g')
        self.serC.write(str(diff2) + 'g')

        #TODO: Always mess around with this value
        sleep(.35)

        pass

    # def dldp(self, nodePos, theta, phi):
    #     ''' use a directional vector and current position to calculate change in node length '''

    #     cam = self.cam
    #     deltaX = cam[0] - nodePos[0]
    #     deltaY = cam[1] - nodePos[1]
    #     deltaZ = cam[2] - nodePos[2]
    #     numer = deltaX*cos(theta)*cos(phi) + deltaY*sin(theta)*cos(phi) + deltaZ*sin(phi)
    #     denom = (deltaX**2 + deltaY**2 + deltaZ**2)**.5
    #     return numer/denom

    def binary_search(self, ustart, s, dl, tol=.01):
        ''' Perform a binary search to find parametrized location of point.

            Inputs:
                ustart: (float)
                s: (spline object)
                dl: (float)
                tol: (float)

            Returns:
                Reassigns middle and endpoints of search
                um: (float) midpoint of search
         '''

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
        ''' Calculate length of a spline.

            Inputs:
                s: (spline object) represents path that joins waypoints

            Returns:
                (float) length of spline
        '''
        ts = np.linspace(0, 1, 1000)
        xs, ys, zs = splev(ts, s)
        spline = zip(xs, ys, zs)

        ipoint = spline[0]
        totl = 0

        for point in spline:
            totl += distance(point, ipoint)
            ipoint = point

        return totl

    def tighten(self):
        ''' Calibrate node lengths to current position of camera.

            Enter ' ' to tighten
            Enter 's' to accept node length
        '''

        while True:
            input = raw_input('Tightening Node A')
            if input == ' ':
                self.serA.write('-100g')
            elif input == 's':
                break

        while True:
            input = raw_input('Tightening Node B')
            if input == ' ':
                self.serB.write('-100g')
            elif input == 's':
                break

        while True:
            input = raw_input('Tightening Node C')
            if input == ' ':
                self.serC.write('-100g')
            elif input == 's':
                return

class Path:
    ''' Path object stores a path's points, node lengths, and length differences
        to enable in path traversal.
    '''

    def __init__(self, points, node0, node1, node2):
        ''' Init method for Path class.

            Input:
                points: (list of tuples of floats)
                node0, 1, 2: (tuple of floats)

            Returns:
                Initializes Path attributes
        '''

        self.points = points

        self.lens0 = [distance(node0, point) for point in points]
        self.lens1 = [distance(node1, point) for point in points]
        self.lens2 = [distance(node2, point) for point in points]

        self.diffs0 = self.diff_calc(self.lens0)
        self.diffs1 = self.diff_calc(self.lens1)
        self.diffs2 = self.diff_calc(self.lens2)

    @staticmethod
    def new_path(points, node0, node1, node2):
        ''' Factory function to create new path object, if it exists within boundary.

            Inputs:
                points: (list of tuples of floats) points that make up a path
                node0, 1, 2: (tuple of floats) coordinates of nodes

            Returns:
                (Path) new initialized Path object
        '''

        #Check if any point lies outside boundary
        for point in points:
            if Path.boundary(node0, node1, node2, point):
                return None

        return Path(points, node0, node1, node2)



    @staticmethod
    def boundary(node0, node1, node2, point, offset=6, hbound=120):
        ''' Check if any given point lies outside the boundaries of our system.

            Inputs:
                node0, 1, 2: (tuple of floats)
                point: (tuple of floats)
                offset: (float) offset distance from nodes to define boundary triangle
                hbound: (float) lower bound of z y-axis

            Returns:
                (bool) Whether point is outside boundary, prints which
        '''

        # Find midpoint of each side
        mid_AB = tuple((node0[i] + node1[i])/2 for i in xrange(3))
        mid_BC = tuple((node1[i] + node2[i])/2 for i in xrange(3))
        mid_AC = tuple((node2[i] + node0[i])/2 for i in xrange(3))

        # Find slope of line connecting point to opposite midpoint
        m_A = tuple((mid - node)/distance(mid_BC, node0) for (mid, node) in zip(mid_BC, node0))
        m_B = tuple((mid - node)/distance(mid_AC, node1) for (mid, node) in zip(mid_AC, node1))
        m_C = tuple((mid - node)/distance(mid_AB, node2) for (mid, node) in zip(mid_AB, node2))

        # Find offset node coordinates
        new_0 = tuple(coord + slope*offset for (coord, slope) in zip(node0, m_A))
        new_1 = tuple(coord + slope*offset for (coord, slope) in zip(node1, m_B))
        new_2 = tuple(coord + slope*offset for (coord, slope) in zip(node2, m_C))

        if point[2] < 0 or point[2] > hbound:
            print 'Height of path out of bounds', point[2]
            return True

        elif point[0] < 0:
            print "Path out of bounds of line AB", point[0]
            return True

        elif point[1] < (new_2[1]*point[0]/new_2[0]):
            print "Path out of bounds of line AC", point[1]
            return True

        elif point[1] > (((new_2[1] - new_1[1])/new_2[0])*point[0] + new_1[1]):
            print "Path out of bounds of line BC", point[1]
            return True

        else:
            return False

    def diff_calc(self, lens):
        ''' Return differences between subsequent spool lengths x100 for sending.

            Input:
                lens: (list of floats) lengths of node wires at any time

            Returns:
                (list of floats) differences between subsequent lengths*100
        '''
        return [int(80*(lens[ind+1] - lens[ind])) for ind in xrange(len(lens)-1)]

def distance(A, B):
    ''' Calculate the distance between two points.

        Inputs:
            A: (tuple of floats/ints) first point
            B: (tuple of floats/ints) second point

        Returns:
            (float) distance between the points
         '''

    dx = A[0] - B[0]
    dy = A[1] - B[1]
    dz = A[2] - B[2]
    return (dx**2 + dy**2 + dz**2)**.5