from opyscad import *
import config


diameter = 260.0
plate_thickness = 3.0
glass_thickness = 3.0
bar2bed_h = 4.0
height = config.bottom_height + bar2bed_h

d = 265.0
hole_d = 3.2
w = 100.0
l = d/2 + 5

hole_dx = 8.0
hole_dy = 7.0

full_height = height + plate_thickness + glass_thickness


def create():
	res = union()
	s = cube([l, w, plate_thickness]) << [0, -w/2, 0]
	
	c = cylinder(5, d = hole_d, fn = 64) << [l - hole_dx, 0, -1]
	
	s -= c << [0, w/2 - hole_dy, 0]
	s -= c << [0, -w/2 + hole_dy, 0]
	
	
	res += s
	res += s / [0, 0, 120]
	res += s / [0, 0, 240]
	
	res += cylinder(h = plate_thickness, d = d, fn = 64)
	
	res = color(config.bedcol) (res)
	
	res += ~cylinder(glass_thickness, d = diameter, fn = 64) << [0, 0, glass_thickness + 0.01]
	
	return res << [0, 0, height]
	