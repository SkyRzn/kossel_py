from opyscad import *
from config import *
import math


def trapeze(h, r, x1, x2, y):
	dx = y*(math.sin(math.pi/6))
	x1 = x1 - dx
	x2 = x2 - dx
	corner = cylinder(h, r, fn = 64)
	a = (corner << [x1, -y, 0]) / [0, 0, 30]
	b = (corner << [x1, y, 0]) / [0, 0, -30]
	c = (corner << [x2, -y, 0]) / [0, 0, 30]
	d = (corner << [x2, y, 0]) / [0, 0, -30]
	return hull() (a, b, c, d)

def hbar_screw(x, z, side):
	scr = vertex.hbar_screw.hole(vertex.thickness + 2, vertex.thickness + 2) / [90 * side, 0, 0]
	x += vertex.hbar_offset_x
	y = (vertex.hbar_offset_y - bar.width/2 - vertex.thickness + vertex.screw_cap_depth) * side
	res = scr << [x, y, z]

	return (res / [0, 0, 30 * side])

def screws(z):
	res = hbar_screw(vertex.hbar_screw_x1, z, 1)
	res += hbar_screw(vertex.hbar_screw_x1, z, -1)

	res += hbar_screw(vertex.hbar_screw_x2, z, 1)
	res += hbar_screw(vertex.hbar_screw_x2, z, -1)

	if vertex.hbar_end_screws:
		scr = vertex.hbar_screw.hole(vertex.thickness + 2, vertex.hbar_offset_x + bar.width) / [90, 0, 0]
		scr <<= [-vertex.hbar_offset_y, vertex.hbar_offset_x - vertex.thickness, z]
		res += scr / [0, 0, -60]
		scr <<= [vertex.hbar_offset_y * 2, 0, 0]
		res += scr / [0, 0, -120]
	return res

def z_screw(z, side):
	scr = vertex.vbar_screw.hole(vertex.thickness + 1, bar.width) / [90 * side, 0, 0]
	y = (-bar.width/2 - vertex.thickness - bar.gap) * side
	return scr << [0, y, z]

def z_screws(z):
	res = z_screw(z, 1)
	res += z_screw(z, -1)
	return res

def create_vertex(h, bottom = False, extra_height = 0):
	h2 = h + extra_height
	vert = cube([bar.width, bar.width + vertex.thickness * 2, h2]) << [-bar.width/2, -bar.width/2 - vertex.thickness, 0]

	edge = cube([vertex.hbar_mount_len, bar.width, h]) << [vertex.hbar_offset_x - 0.01, -bar.width/2, 0]
	edge1 = (edge << [0, vertex.hbar_offset_y, 0]) / [0, 0, 30]
	edge2 = (edge << [0, -vertex.hbar_offset_y, 0]) / [0, 0, -30]

	res = hull() (vert, edge1, edge2)

	vert = cube([bar.width + 1, bar.width + bar.gap*2, h2 + 2])
	res -= vert << [-bar.width/2 - 1, -bar.width/2 - bar.gap, -1]

	#### cut edge profile
	edge = cube([vertex.hbar_mount_len, bar.width + 1, h2 + 2]) << [vertex.hbar_offset_x, -bar.width/2, -1]
	res -= (edge << [0, vertex.hbar_offset_y, 0]) / [0, 0, 30]
	res -= (edge << [0, -vertex.hbar_offset_y - 1, 0]) / [0, 0, -30]

	#### windows
	y = -vertex.hbar_offset_y + bar.width/2 + vertex.window_r + vertex.thickness
	mx = 1.0/(math.cos(math.pi/6))

	x1 = (bar.width/2 + vertex.window_r + vertex.thickness) * mx
	x2 = vertex.hbar_offset_x + vertex.hbar_mount_len/2 - (vertex.thickness/2 + vertex.window_r)*mx
	res -= trapeze(h2 + 2, vertex.window_r, x1, x2, y) << [0, 0, -1]

	x1 = vertex.hbar_offset_x + vertex.hbar_mount_len/2 + (vertex.thickness/2 + vertex.window_r)*mx
	x2 = vertex.hbar_mount_len + vertex.hbar_offset_x
	res -= trapeze(h2 + 2, vertex.window_r, x1, x2, y) << [0, 0, -1]

	#### cut ends
	cut = cube([vertex.thickness + 1, vertex.thickness + 2, h + 2])
	cut <<= [vertex.hbar_offset_x + vertex.hbar_mount_len - vertex.thickness, 0, -1]
	res -= (cut << [0, vertex.hbar_offset_y - bar.width/2 - vertex.thickness - 1, 0]) / [0, 0, 30]
	res -= (cut << [0, -vertex.hbar_offset_y + bar.width/2 - 1, 0]) / [0, 0, -30]

	#### screws
	if bottom:
		res -= screws(bar.width/2)
		res -= screws(h - bar.width/2)
	else:
		res -= screws(h/2)

	res -= z_screws(vertex.vbar_screw_distance)
	res -= z_screws(h2 - vertex.vbar_screw_distance)

	return res

