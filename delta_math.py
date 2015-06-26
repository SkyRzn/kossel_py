import math
from config import *
import bar #TODO remove dependence
import rod, carriage, effector, rail
import vertex


def points_dist(p1, p2):
	return math.sqrt(sum([(x1 - x2)*(x1 - x2) for x1, x2 in zip(p1, p2)]))

def rotate(a, fi):
	fi = fi/180.0*math.pi
	x = a[0] * math.cos(fi) - a[1] * math.sin(fi)
	y = a[0] * math.sin(fi) + a[1] * math.cos(fi)
	return (x, y)

def calc_z(col, x, y, z):
	l = rod.length
	colx, coly = col
	dx = (colx - x)
	dy = (coly - y)

	sqr_res = l*l - dx*dx - dy*dy
	if sqr_res < 0:
		return None

	return z + math.sqrt(sqr_res)

def inverse(p):
	x, y, z = p
	cx = -vertex.base_center2vertex() + bar.width/2 + rail.rod_mount_dx
	cy = 0.0

	res = []
	for fi in [0, 120, 240]:
		rx, ry = rotate((cx + effector.rod_dx, cy), fi)
		rz = calc_z((rx, ry), x, y, z)
		if rz == None:
			return None
		rx, ry = rotate((cx, cy), fi)
		res.append([rx, ry, rz])

	return res



