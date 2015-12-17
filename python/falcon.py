from Skycam import Skycam, Path, distance
from numpy import pi, cos, sin

cam = (50, 70, 95) #111
a = 154.25
b = 157.5
c = 138
zB = 0.75
zC = 3.0
skycam = Skycam(a, b, c, zB, zC, cam)
# waypoints = [(10, 30, 5), (15, 30, 5)]

'''Various individual path options'''
goin_up = [(cam[0], cam[1], cam[2] - i) for i in xrange(20)]
goin_down = list(reversed(goin_up))
goin_to = [(cam[0], cam[1] + 1.5*i, 75) for i in xrange(10)]
goin_fro = list(reversed(goin_to))
thetas = [((pi/2) + (m*pi/40)) for m in xrange(81)]
goin_circle = [(cam[0] + 15*cos(theta), cam[1] + 15*sin(theta), 75) for theta in thetas]
phis = [((pi/2) + (m*pi/40)) for m in xrange(321)]
goin_spiral = [(cam[0] + 20*cos(phi), cam[1] + 20*sin(phi), 95 - (phi/pi - .5)) for phi in phis]
goin_spiral_reverse = list(reversed(goin_spiral))


'''Various path combinations'''
# goin_somewhere = point_2_point(cam, (,,,), (20, 30, 70))

# path = goin_up + goin_to + goin_circle + goin_fro + goin_down
# path = goin_up + [goin_up[-1]] + goin_to + [goin_to[-1]] + goin_circle + goin_fro + [goin_fro[-1]] + goin_down
# path = goin_up + 8*[goin_to[0]] + goin_to + 20*[goin_circle[0]] + goin_circle + 30*[goin_fro[0]] + goin_fro + 8*[goin_down[0]] + goin_down
# path = goin_to + 20*[goin_spiral[0]] + goin_spiral + [goin_spiral_reverse[0]] + goin_spiral_reverse + 20*[goin_fro[0]] + goin_fro
path = goin_up + 2*[goin_up[-1]] + goin_to + 2*[goin_to[-1]] + goin_circle + goin_fro + 2*[goin_fro[-1]] + goin_down

# Perform the proper setup and then fly
skycam.load_path(path)
skycam.connect()
skycam.tighten()
skycam.go_path(skycam.save_point)

def point_2_point(A, B):
    ''' Generate a path from point A to point B.

        Inputs:
            A: (tuple of floats) the initial coordinate
            B: (tuple of floats) the final coordinate

        Returns:
            (list of tuples) list of points from A to B
    '''

    difx = B[0] - A[0]
    dify = B[1] - A[1]
    difz = B[2] - A[2]

    dl = round(max([abs(difx), abs(dify), abs(difz)]))
    dx = difx/dl
    dy = dify/dl
    dz = difz/dl
    iter = xrange(int(dl)+1)

    return [(cam[0] + dx*i, cam[1] + dy*i, cam[2] + dz*i) for i in iter]
