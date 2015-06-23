#!/usr/bin/python


from opyscad import *
from config import *


h = bed.thickness
d = 265.0
hole_d = 3.2


def create_bed():
	res = union()
	s = cube([d/2 + 5, 100, h]) << [0, -50, 0]
	
	c = +cylinder(5, d = hole_d, fn = 64) << [d/2 - 8, 0, -1]
	
	s -= c << [0, 50 - 7, 0]
	s -= c << [0, -50 + 7, 0]
	
	
	res += s
	res += s / [0, 0, 120]
	res += s / [0, 0, 240]
	
	res += cylinder(h = h, d = d)
	
	res += ~cylinder(h, d = bed.diameter, fn = 64) << [0, 0, 3.3]

	
	return res
	