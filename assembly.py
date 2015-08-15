#!/usr/bin/python


from opyscad import *
import config, vertex, top_vertex, bottom_vertex, bar, bed, endstop, endstop_mount
import rail, kinematics, belt, motor, pulley, bearing, idler, bed_mount


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
	vert = top_vertex.create()
	vert += top_vertex.create_cap()
	vert <<= [-vertex.base_center2vertex(), 0, 0]
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
	maxz = config.vbar_len + idler.dz

	x = -vertex.base_center2vertex() + bar.width/2 + rail.belt_dx

	res = union()
	for fi in [0, 120, 240]:
		part = union()
		part += belt.create(minz, maxz)
		part += bearing.create_couple() << [0, 0, maxz]
		part += idler.create_couple() << [0, 0, maxz]
		part += idler.create_knob() << [0, 0, config.vbar_len + vertex.cap_t]
		part += motor.create() << [motor.pulley_dx, 0, minz]
		part += pulley.create() << [0, 0, minz]
		res += (part << [x, 0, 0]) / [0, 0, fi]
	return res

def create_walls():
	y = -vertex.base_center2edge() - vertex.hbar_offset_y - bar.width/2
	res = union()
	wall = ~cube([config.hbar_len, 1, config.vbar_len - config.bottom_height - bar.width])
	wall <<= [-config.hbar_len/2, y, config.bottom_height]
	res += wall / [0, 0, 90]
	res += wall / [0, 0, -30]
	res += wall / [0, 0, 210]
	return res

def create_endstops():
	x = -vertex.base_center2vertex() + bar.width/2 + 5
	res = (+endstop.create()) << [x, -15, 700]
	return res

def create_bed_mounts():
	mount = bed_mount.create()
	mount <<= [bed.l - bed.hole_dx, 0, config.bottom_height]
	res = mount 
	res += mount / [0, 0, 120]
	res += mount / [0, 0, 240]
	return res


x = 0
y = 0
z = 200

res = union()
res += vert_bars()
res += create_top_frame()
res += create_bottom_frame()
res += bed.create()
res += create_bed_mounts()
res += kinematics.create([x, y, z])
res += create_belt_subsystem()
#res += create_walls()
res += create_endstops()

res.save('scad/assembly.scad')



