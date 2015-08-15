#!/usr/bin/python

from opyscad import *
import bearing, screw, config
import math, copy


l = 30.0
t = 4.0
belt_gap = 2
w = bearing.D1 + t * 2 + belt_gap * 2.0
dx = bearing.D1 / 2
lip_t = 1.5
lip_d = bearing.d + 4.0
bearing_gap = 0.0
cap_gap = 0.2
h = t + bearing.B + lip_t + bearing_gap
bearing_nut = screw.m3
bearing_nut_depth = 2.6
bearing_screw_head_depth = 2.6

dz = -45.0


knob_d = 40.0
knob_h = 12.0
knob_cut_r = 1
knob_cut_steps = 40
knob_nut_h = 2.0
knob_trigger_dist = 17.0
knob_trigger_d = 2.0
knob_triger_depth = 0.5
knob_trigger_steps = 40
trigger_gap = 0.2
knob_nut = copy.copy(screw.m6)
knob_nut.gap_thread = 0.1
knob_nut.gap_octo = 0.3

screw_head_h = 5.5
screw_h = 50.0
screw_x = 16.0

const_screw = screw.m3
const_screw_dist_x = 4.5
const_screw_dist_y = 4.5
const_screw_head_depth = 3.3
const_nut_depth = 4.0

print w, h*2
def create(octo_nut = True):
	if octo_nut:
		scr_depth = bearing_nut_depth
	else:
		scr_depth = bearing_screw_head_depth

	res = cube([l, w, h]) << [-dx, -w/2, 0]
	res -= cube([bearing.D1 + belt_gap*2, bearing.D1 + belt_gap*2, bearing.B + lip_t + bearing_gap + 1]) << [-dx-1, -bearing.D1/2 - belt_gap, t]
	res += cylinder(lip_t, d = lip_d, fn = 24) << [0, 0, t - 0.01]
	scr = bearing_nut.hole(t + lip_t + 1, scr_depth + 1, octo = octo_nut) / [180, 0, 0]
	res -= scr << [0, 0, scr_depth]
	#res -= +bearing_nut.hole(t + lip_t + 1, scr_depth + 1, octo = octo_nut) << [0, 0, -1]
	res += +bearing_nut.z_sup(scr_depth)
	#res -= cylinder(t + lip_t + 2, d = bearing.d + 0.5, fn = 16) << [0, 0, -1]
	
	bolt = +knob_nut.hole(screw_h, screw_head_h, octo = True) / [0, -90, 0]
	bolt /= [90, 0, 0]
	bolt <<= [screw_x, 0, h]
	res -= bolt

	if octo_nut:
		scr_depth = const_nut_depth
	else:
		scr_depth = const_screw_head_depth
	
	scr = const_screw.hole(h + 1, scr_depth + 1, octo = octo_nut) / [180, 0, 0]
	res -= scr << [l-dx - const_screw_dist_x, w/2 - const_screw_dist_y, scr_depth]
	res -= scr << [l-dx - const_screw_dist_x, -w/2 + const_screw_dist_y, scr_depth]
	sup = +const_screw.z_sup(scr_depth)
	res += sup << [l-dx - const_screw_dist_x, w/2 - const_screw_dist_y, 0]
	res += sup << [l-dx - const_screw_dist_x, -w/2 + const_screw_dist_y, 0]
	
	return res

def create_couple():
	dx = t + lip_t + bearing.B
	res = (create() / [0, -90, 0]) << [dx + bearing_gap, 0, 0]
	res += (create() / [180, -90, 0]) << [-dx - bearing_gap, 0, 0]
	return res

def create_knob(printing = False):
	res = cylinder(knob_h, d = knob_d, fn = 128)
	
	cut = cylinder(knob_h + 2, knob_cut_r, fn = 16) << [knob_d/2, 0, -1]
	cut += (cube([2, 10, 4], center = True) / [0, -30, 0]) << [knob_d/2, 0, knob_h]
	cut += (cube([1, 10, 4], center = True) / [0, 30, 0]) << [knob_d/2, 0, 0]
	for i in range(knob_cut_steps):
		fi = 360.0/knob_cut_steps*i
		res -= cut / [0, 0, fi]

	if printing:
		res += create_trigger(False)

	res -= knob_nut.hole(knob_nut_h + 1, knob_h, octo = True) << [0, 0, knob_nut_h]
	res += knob_nut.z_sup(knob_h - knob_nut_h + 0.1) << [0, 0, knob_nut_h - 0.1]
	print knob_h - knob_nut_h
	return color(config.knobcol) (res)

def create_trigger(gap):
	gap_r = 0
	if gap:
		gap_r = trigger_gap
	res = union()
	trigger = sphere(d = knob_trigger_d + gap_r*2, fn = 16)
	trigger <<= [knob_trigger_dist, 0, knob_triger_depth]
	for i in range(knob_trigger_steps):
		fi = 360.0/knob_trigger_steps*i
		res += trigger / [0, 0, fi]
	return res

if 1: #__name__ == '__main__':
	res = create(False)
	res += create(True) << [0, w + 10, 0]
	res.save('scad/idler.scad')
	
	res = (create_knob(True) / [180, 0, 0]) << [0, 0, knob_h]
	res.save('scad/knob.scad')
