from opyscad import *
import vertex, bar, rail, rod, effector, bed
from delta_math import inverse


def create(p):
	p[2] = p[2] + bed.full_height + effector.ext_dz
	res = union()

	carriages = inverse(p)
	if not carriages:
		return +sphere(30) << p

	p2 = p[:]
	p2[0] -= 1
	carriages2 = inverse(p2)

	for i, fi in enumerate([0, 120, 240]):
		r = rail.create(carriages[i][2])
		r <<= [-vertex.base_center2vertex() + bar.width/2, 0, 0]
		res += r / [0, 0, fi]
		res += rod.create(p, carriages[i], fi)
		print carriages[i][2] - carriages2[i][2]

	res += effector.create(p)

	return res



