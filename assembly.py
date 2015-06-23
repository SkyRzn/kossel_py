#!/usr/bin/python


from opyscad import *
from config import *
from top_vertex import create_top_vertex
from bottom_vertex import create_bottom_vertex
from profile import profile
from mgn_12h import MGN_12H_rail, MGN_12H_block
from bed import create_bed


def hor_bars():
	hbar = profile(main.hbar_len) / [90, 0, 90]
	hbar <<= [-main.hbar_len/2, -vertex.base_center2edge() - vertex.hbar_offset_y + 0.01, bar.width/2 + 0.01]

	res = hbar / [0, 0, -30]
	res += hbar / [0, 0, 90]
	res += hbar / [0, 0, 210]

	return res

def vert_bars():
	vbar = profile(main.vbar_len)
	vbar <<= [-vertex.base_center2vertex() - 0.01, 0, 0.01]

	res = vbar
	res += vbar / [0, 0, 120]
	res += vbar / [0, 0, -120]

	return res

def create_top_frame():
	vert = create_top_vertex() << [-vertex.base_center2vertex(), 0, 0]
	vert = color([1, 0.5, 0]) (vert)
	vert /= [180, 0, 0]
	vert <<= [0, 0, bar.width]

	frame = vert
	frame += vert / [0, 0, 120]
	frame += vert / [0, 0, -120]

	frame += hor_bars()

	return frame << [0, 0, main.vbar_len - bar.width]

def create_bottom_frame():
	vert = create_bottom_vertex() << [-vertex.base_center2vertex(), 0, 0]
	vert = color([1, 0.5, 0]) (vert)

	frame = vert
	frame += vert / [0, 0, 120]
	frame += vert / [0, 0, -120]

	frame += hor_bars()
	frame += hor_bars() << [0, 0, vertex.bottom_height - bar.width]

	return frame

def create_rail(length, z):
	res = MGN_12H_rail(length)
	res += MGN_12H_block() << [0, 0, z]
	return res

def create_rails():
	r = create_rail(rail.length, rail.length/2)
	r <<= [-vertex.base_center2vertex() + bar.width/2, 0, 0]

	res = r
	res += r / [0, 0, 120]
	res += r / [0, 0, -120]

	res <<= [0, 0, rail.z]

	return res

res = union()

res += vert_bars()

res += create_top_frame()

res += create_bottom_frame()

res += create_rails()

res += create_bed() << [0, 0, bed.height]

res.save('assembly.scad')
