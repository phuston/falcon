from Skycam import Skycam, Path, distance
from numpy import pi, cos, sin
cam = (50, 70, 100) #111
a = 154.25
b = 157.5
c = 138
zB = 0.75
zC = 3.0
skycam = Skycam(a, b, c, zB, zC, cam)
# waypoints = [(10, 30, 5), (15, 30, 5)]
goin_up = [(cam[0], cam[1], cam[2] - i) for i in xrange(40)]
goin_down = list(reversed(goin_up))
goin_fro = [(cam[0], cam[1] + 1.5*i, 80) for i in xrange(10)]
goin_to = list(reversed(goin_fro))
thetas = [((pi/2) + (m*pi/30)) for m in xrange(61)]
goin_circle = [(cam[0] + 15*cos(theta), cam[1] + 15*sin(theta), 0) for theta in thetas]
path = goin_fro + goin_circle + goin_to#goin_up + goin_fro + goin_circle + goin_to + goin_down
print path
skycam.load_path(path)
skycam.connect()
skycam.tighten()
skycam.go_path()


