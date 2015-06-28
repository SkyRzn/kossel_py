from opyscad import *


l = 40.0
h  = 16.5
t = 2.0
sw_l = 14.0
sw_h = 7.0
sw_t = 4.0
sw_offs = 7.0


def create():
	res = cube([t, l, h])
	res += cube([sw_t, sw_l, sw_h]) << [t-0.1, sw_offs, 0]
	res += cube([3, 2, 10]) << [t, sw_offs-2, -5]
	res << [0, l/2, 0]
	return res

