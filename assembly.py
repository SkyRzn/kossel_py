#!/usr/bin/python


from opyscad import *
from config import *
from top_vertex import top_vertex
from bottom_vertex import bottom_vertex
import math


d = edge_full_len/2/math.cos(math.pi/6)
d2 = edge_full_len*math.cos(math.pi/6) - d


def hor_edges():
	edge = cube([edge_len, profile_w, profile_w])
	edge <<= [-edge_len/2, -profile_w/2 - d2 - edge_offset_y - 0.1, -0.01]

	res = edge / [0, 0, -30]
	res += edge / [0, 0, 90]
	res += edge / [0, 0, 210]

	return res

def vert_edges():
	v_edge = cube([profile_w, profile_w, height]) << [-profile_w/2, -profile_w/2, 0.01]
	v_edge <<= [-d, 0, 0]

	res = v_edge
	res += v_edge / [0, 0, 120]
	res += v_edge / [0, 0, -120]

	return res

def top_frame():
	vertex = top_vertex() << [-d, 0, 0]
	vertex = color([1, 0.5, 0]) (vertex)

	frame = vertex
	frame += vertex / [0, 0, 120]
	frame += vertex / [0, 0, -120]

	frame += hor_edges()

	return frame << [0, 0, height - profile_w]

def bottom_frame():
	vertex = bottom_vertex() << [-d, 0, 0]
	vertex = color([1, 0.5, 0]) (vertex)

	frame = vertex
	frame += vertex / [0, 0, 120]
	frame += vertex / [0, 0, -120]

	frame += hor_edges()
	frame += hor_edges() << [0, 0, bottom_h - profile_w]

	return frame

res = vert_edges()

res += top_frame()

res += bottom_frame()

res += ~cylinder(bed_t, d = bed_d) << [0, 0, bed_h]

res.save('assembly.scad')
