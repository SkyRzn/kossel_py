#!/usr/bin/python


from opyscad import *
import config, vertex, top_vertex, bottom_vertex, bar, bed, rail, kinematics, belt, motor, tensioner, pulley, bearing


def hor_bars():
	hbar = bar.create(config.hbar_len) / [90, 0, 90]
	hbar <<= [-config.hbar_len/2, -vertex.base_center2edge() - vertex.hbar_offset_y + 0.01, bar.width/2 + 0.01]

	res = hbar / [0, 0, -30]
	res += hbar / [0, 0, 90]
	res += hbar / [0, 0, 210]

	return res

def vert_bars():
	vbar = bar.create(config.vbar_len)
	vbar <<= [-vertex.base_center2vertex() - 0.01, 0, 0.01]

	res = vbar
	res += vbar / [0, 0, 120]
	res += vbar / [0, 0, -120]

	return res

def create_top_frame():
	vert = top_vertex.create() << [-vertex.base_center2vertex(), 0, 0]
	vert /= [180, 0, 0]
	vert <<= [0, 0, bar.width]

	frame = vert
	frame += vert / [0, 0, 120]
	frame += vert / [0, 0, -120]

	frame += hor_bars()

	return frame << [0, 0, config.vbar_len - bar.width]

def create_bottom_frame():
	vert = bottom_vertex.create() << [-vertex.base_center2vertex(), 0, 0]

	frame = vert
	frame += vert / [0, 0, 120]
	frame += vert / [0, 0, -120]

	frame += hor_bars()
	frame += hor_bars() << [0, 0, config.bottom_height - bar.width]

	return frame

def create_belt_subsystem():
	minz = motor.dz
	maxz = config.vbar_len + tensioner.idler_dz

	x = -vertex.base_center2vertex() + bar.width/2 + rail.belt_dx

	res = union()
	for fi in [0, 120, 240]:
		part = belt.create(minz, maxz)
		part += bearing.create_couple() << [0, 0, maxz]
		part += motor.create() << [motor.pulley_dx, 0, minz]
		part += pulley.create() << [0, 0, minz]
		res += (part << [x, 0, 0]) / [0, 0, fi]
	return res

x = 0
y = 0
z = 0

res = union()
res += vert_bars()
res += create_top_frame()
res += create_bottom_frame()
res += bed.create()
res += kinematics.create([x, y, z])
res += create_belt_subsystem()

res.save('scad/assembly.scad')



