from opyscad import *

import config

diameter = 260.0
plate_thickness = 3.0
glass_thickness = 3.0
height = config.bottom_height + 2.0

d = 265.0
hole_d = 3.2

full_height = height + plate_thickness + glass_thickness

def create():
	res = union()
	s = cube([d/2 + 5, 100, plate_thickness]) << [0, -50, 0]
	
	c = +cylinder(5, d = hole_d, fn = 64) << [d/2 - 8, 0, -1]
	
	s -= c << [0, 50 - 7, 0]
	s -= c << [0, -50 + 7, 0]
	
	
	res += s
	res += s / [0, 0, 120]
	res += s / [0, 0, 240]
	
	res += cylinder(h = plate_thickness, d = d)
	
	res += ~cylinder(glass_thickness, d = diameter, fn = 64) << [0, 0, glass_thickness + 0.01]
	
	return res << [0, 0, height]
	