from Skycam import Skycam, Path, distance
from numpy import pi, cos, sin
cam = (50, 70, 111)
a = 154.25
b = 157.5
c = 138
zB = 0.75
zC = 3.0
skycam = Skycam(a, b, c, zB, zC, cam)
# waypoints = [(10, 30, 5), (15, 30, 5)]
goin_up = [(cam[0], cam[1], cam[2] - i) for i in xrange(30)]
goin_down = list(reversed(goin_up))
goin_fro = [(cam[0], cam[1] + .5*i, 91) for i in xrange(20)]
goin_to = list(reversed(goin_fro))
thetas = [((pi) + (m*pi/50)) for m in xrange(101)]
goin_circle = [(cam[0] + 10*cos(theta), cam[1] + 10*sin(theta), 91) for theta in thetas]
path = goin_up + goin_fro + goin_to + goin_down
print path
skycam.load_path(path)
skycam.connect()
skycam.tighten_A()
skycam.tighten_B()
skycam.tighten_C()
skycam.go_path()


