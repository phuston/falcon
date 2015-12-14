from Skycam import Skycam, Path, distance

cam = (1, 1, 30)
a =
b =
c =
zB =
zC =
skycam = Skycam(a, b, c, zB, zC, cam)
waypoints = [(10, 30, 5), (15, 30, 5)]
goin_up = [(cam[0], cam[1], cam[2] - .5*i) for i in xrange(30)]
goin_down = list(reversed(goin_up))
path = goin_up + goin_down
print path
skycam.load_path(path)
skycam.connect()
skycam.tighten_A()
skycam.tighten_B()
skycam.tighten_C()


# skycam.go_path()