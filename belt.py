from opyscad import *
import bearing


w = 6.0
t = 1.0
dx = 20.0


def create(minz, maxz):
	res = cube([w, t, maxz - minz]) << [-w/2, bearing.D/2 - t, minz]
	res += cube([w, t, maxz - minz]) << [-w/2, -bearing.D/2, minz]
	return color([0.1, 0.1, 0.1]) (res)



