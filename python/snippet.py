from Skycam import Skycam, Path, distance
from numpy import pi, cos, sin

cam = (50, 70, 95)
a = 154.25
b = 157.5
c = 138
zB = 0.75
zC = 3.0
skycam = Skycam(a, b, c, zB, zC, cam)

going_up = [(cam[0], cam[1], cam[2] - i) for i in xrange(20)]
going_down = list(reversed(going_up))

going_to = [(cam[0], cam[1] + 1.5*i, 75) for i in xrange(10)]
going_fro = list(reversed(going_to))

thetas = [((pi/2) + (m*pi/40)) for m in xrange(81)]
going_circle = [(cam[0] + 15*cos(theta), cam[1] + 15*sin(theta), 75) for theta in thetas]

path = going_up + going_to + going_circle + going_fro + going_down
skycam.load_path(path)
skycam.connect()
skycam.tighten()
skycam.go_path(skycam.save_point)