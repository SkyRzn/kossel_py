from opyscad import *
from config import *
import math


def trapeze(h, r, x1, x2, y):
	dx = y*(math.sin(math.pi/6))
	x1 = x1 - dx
	x2 = x2 - dx
	corner = cylinder(h, r, fn = corner_fn)
	a = (corner << [x1, -y, 0]) / [0, 0, 30]
	b = (corner << [x1, y, 0]) / [0, 0, -30]
	c = (corner << [x2, -y, 0]) / [0, 0, 30]
	d = (corner << [x2, y, 0]) / [0, 0, -30]
	return hull() (a, b, c, d)

def screw(d1, h1, d2, h2):
	res = cylinder(h1+0.01, d = d1, fn = screw_fn) << [0, 0, -h1]
	res += cylinder(h2, d = d2, fn = screw_fn) << [0, 0, 0]
	return res

def z_screw(z, side):
	scr = screw(edge_screw_d1, vertex_t + 1, edge_screw_d2, profile_w)
	scr /= [90 * side, 0, 0]
	y = (-profile_w/2 - vertex_t - profile_gap) * side
	return scr << [0, y, z]

def edge_screw(x, z, side):
	scr = screw(edge_screw_d1, vertex_t + 2, edge_screw_d2, vertex_t + 2) / [90 * side, 0, 0]
	x += edge_offset_x
	y = (edge_offset_y - profile_w/2 - vertex_t + edge_screw_t) * side
	scr <<= [x, y, z]
	return (scr / [0, 0, 30 * side])

def screws(z):
	res = z_screw(z, 1)
	res += z_screw(z, -1)

	res += edge_screw(edge_screw1_x, z, 1)
	res += edge_screw(edge_screw1_x, z, -1)

	res += edge_screw(edge_screw2_x, z, 1)
	res += edge_screw(edge_screw2_x, z, -1)

	return res

def vertex(h, bottom = False):
	vert = cube([profile_w, profile_w + vertex_t * 2, h]) << [-profile_w/2, -profile_w/2 - vertex_t, 0]

	edge = cube([vertex_l, profile_w, h]) << [edge_offset_x - 0.01, -profile_w/2, 0]
	edge1 = (edge << [0, edge_offset_y, 0]) / [0, 0, 30]
	edge2 = (edge << [0, -edge_offset_y, 0]) / [0, 0, -30]

	res = hull() (vert, edge1, edge2)

	vert = cube([profile_w + 1, profile_w + profile_gap*2, h + 2])
	res -= vert << [-profile_w/2 - 1, -profile_w/2 - profile_gap, -1]

	#### cut edge profile
	edge = cube([vertex_l, profile_w + 1, h + 2]) << [edge_offset_x, -profile_w/2, -1]
	res -= (edge << [0, edge_offset_y, 0]) / [0, 0, 30]
	res -= (edge << [0, -edge_offset_y - 1, 0]) / [0, 0, -30]

	#### windows
	y = -edge_offset_y + profile_w/2 + window_r + vertex_t
	mx = 1.0/(math.cos(math.pi/6))

	x1 = (profile_w/2 + window_r + vertex_t) * mx
	x2 = edge_offset_x + vertex_l/2 - (vertex_t/2 + window_r)*mx
	res -= trapeze(h + 2, window_r, x1, x2, y) << [0, 0, -1]

	x1 = edge_offset_x + vertex_l/2 + (vertex_t/2 + window_r)*mx
	x2 = vertex_l + edge_offset_x
	res -= trapeze(h + 2, window_r, x1, x2, y) << [0, 0, -1]

	#### cut ends
	cut = cube([vertex_t + 1, vertex_t + 2, h + 2])
	cut <<= [edge_offset_x + vertex_l - vertex_t, 0, -1]
	res -= (cut << [0, edge_offset_y - profile_w/2 - vertex_t - 1, 0]) / [0, 0, 30]
	res -= (cut << [0, -edge_offset_y + profile_w/2 - 1, 0]) / [0, 0, -30]

	#### screws
	if bottom:
		res -= screws(profile_w/2)
		res -= screws(h - profile_w/2)
	else:
		res -= screws(h/2)

	#### cut
	#r = 28
	#x = edge_offset_x/2 - 12
	#y = r + edge_offset_y
	#cut = cylinder(h + 2, r, fn = corner_fn)
	#res -= (cut << [x, y, -1]) / [0, 0, 30]
	#res -= (cut << [x, -y, -1]) / [0, 0, -30]

	return res

