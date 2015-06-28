from opyscad import *
from delta_math import points_dist, rotate
import effector, config


length = 328 #+ 300.0/100*9
d = 5.8


def eff_move_y(p, fi, side):
	offs = [0, effector.rod_dy * side]
	offs = rotate(offs, fi)
	return [p[0] - offs[0], p[1] - offs[1], p[2]]

def eff_move_xy(p, fi, side):
	offs = [effector.rod_dx, effector.rod_dy * side]
	offs = rotate(offs, fi)
	return [p[0] - offs[0], p[1] - offs[1], p[2]]

def create_rod(p1, p2, fi, side):
	p1 = eff_move_xy(p1, fi, side)
	p2 = eff_move_y(p2, fi, side)
	rod1 = sphere(d = d) << p1
	rod2 = sphere(d = d) << p2
	res = hull() (rod1, rod2)

	pdist = round(points_dist(p1, p2), 2)
	rlen = round(length, 2)
	if pdist != rlen:
		print 'rod_length error %.3f != %.3f' % (rlen, pdist)
	return color(config.rodcol) (res)

def create(p1, p2, fi):
	res = create_rod(p1, p2, fi, -1)
	res += create_rod(p1, p2, fi, 1)
	return res

