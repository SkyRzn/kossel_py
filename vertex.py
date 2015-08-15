from opyscad import *
import bar, config, screw, motor, rail, idler
import math


thickness = 4.5
hbar_mount_len = 77.0
hbar_offset_x = 28.0
hbar_offset_y = 25.0 #20
hbar_end_screws = False
window_r = 5.0
top_extra_height = 20.0
hbar_screw_type = screw.m5
vbar_screw_type = screw.m5
vbar_screw_distance = 7.0
screw_cap_depth = 1.5
hbar_screw_x1 = 7.0
hbar_screw_x2 = 66.0
corner_cut_r = 0.7
ends_disks_h = 0.4
top_septum_x = 65.0
cap_t = 4.0
idler_slot_t = 3.0
idler_slot_h = 45.0

def base_edge_len():
	return config.hbar_len + hbar_offset_x * 2
def base_center2vertex():
	return base_edge_len()/2/math.cos(math.pi/6)
def base_center2edge():
	return base_edge_len() * math.cos(math.pi/6) - base_center2vertex()


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
	scr = hbar_screw_type.hole(thickness + 2, thickness + 2, 10, 9.0) / [90 * side, 0, 0]
	x += hbar_offset_x
	y = (hbar_offset_y - bar.width/2 - thickness + screw_cap_depth) * side
	res = scr << [x, y, z]

	return (res / [0, 0, 30 * side])

def screws(z):
	res = hbar_screw(hbar_screw_x1, z, 1)
	res += hbar_screw(hbar_screw_x1, z, -1)

	res += hbar_screw(hbar_screw_x2, z, 1)
	res += hbar_screw(hbar_screw_x2, z, -1)

	if hbar_end_screws:
		scr = hbar_screw_type.hole(thickness + 2, hbar_offset_x + bar.width) / [90, 0, 0]
		scr <<= [-hbar_offset_y, hbar_offset_x - thickness, z]
		res += scr / [0, 0, -60]
		scr <<= [hbar_offset_y * 2, 0, 0]
		res += scr / [0, 0, -120]
	return res

def z_screw(z, side):
	scr = vbar_screw_type.hole(thickness + 1, bar.width) / [90 * side, 0, 0]
	y = (-bar.width/2 - thickness - bar.gap + screw_cap_depth) * side
	return scr << [0, y, z]

def z_screws(z):
	res = z_screw(z, 1)
	res += z_screw(z, -1)
	return res

def create(h, bottom = False, extra_height = 0, ends_disks_r = 0):
	dz = -1
	h2 = h + extra_height
	
	vert = cube([bar.width, bar.width + thickness * 2, h2]) << [-bar.width/2, -bar.width/2 - thickness, 0]

	edge = cube([hbar_mount_len, bar.width, h]) << [hbar_offset_x - 0.01, -bar.width/2, 0]
	edge1 = (edge << [0, hbar_offset_y, 0]) / [0, 0, 30]
	edge2 = (edge << [0, -hbar_offset_y, 0]) / [0, 0, -30]

	res = hull() (vert, edge1, edge2)
	
	vert = cube([bar.width + 1 + bar.gap, bar.width + bar.gap*2, h2 + 2])
	res -= vert << [-bar.width/2 - 1, -bar.width/2 - bar.gap, -1]

	#### cut edge profile
	edge = cube([hbar_mount_len + 2, bar.width + 1, h2 + 2]) << [hbar_offset_x - bar.gap, -bar.width/2, dz - bar.gap]
	res -= (edge << [0, hbar_offset_y - bar.gap, 0]) / [0, 0, 30]
	res -= (edge << [0, -hbar_offset_y - 1 + bar.gap, 0]) / [0, 0, -30]
	
	#### cut corners
	cut = cylinder(h2 + 2, corner_cut_r, fn = 16) << [0, 0, -1]
	res -= (cut << [hbar_offset_x, -hbar_offset_y + bar.width/2, 0]) / [0, 0, -30]
	res -= (cut << [hbar_offset_x, hbar_offset_y - bar.width/2, 0]) / [0, 0, 30]
	res -= cut << [bar.width/2, bar.width/2, 0]
	res -= cut << [bar.width/2, -bar.width/2, 0]
	
	#### windows
	y = -hbar_offset_y + bar.width/2 + window_r + thickness
	mx = 1.0/(math.cos(math.pi/6))

	if bottom:
		septum_x = bar.width/2 + rail.belt_dx + motor.pulley_dx
	else:
		septum_x = top_septum_x
	x1 = (bar.width/2 + window_r + thickness) * mx
	x2 = (septum_x - thickness - window_r) * mx
	res -= trapeze(h2 + 2, window_r, x1, x2, y) << [0, 0, -1]

	x1 = (septum_x + window_r)*mx
	x2 = hbar_mount_len + hbar_offset_x
	res -= trapeze(h2 + 2, window_r, x1, x2, y) << [0, 0, -1]

	if bottom:
		cut = cylinder(h = thickness + 2, d = motor.lip_cutout_d, fn = 32) / [0, 90, 0]
		res -= cut << [septum_x - thickness - 1, 0, motor.dz]

		cut = motor.screw.hole(thickness + 1, 2, 100, 9.0) / [0, -90, 0]
		cut <<= [septum_x - thickness + 1, 0, motor.dz]

		res -= cut << [0, -motor.screw_dist, -motor.screw_dist]
		res -= cut << [0, -motor.screw_dist, motor.screw_dist]
		res -= cut << [0, motor.screw_dist, -motor.screw_dist]
		res -= cut << [0, motor.screw_dist, motor.screw_dist]

	#### cut ends
	cut = cube([thickness + 1, thickness + 2, h + 2])
	cut <<= [hbar_offset_x + hbar_mount_len - thickness, 0, -1]
	res -= (cut << [0, hbar_offset_y - bar.width/2 - thickness - 1, 0]) / [0, 0, 30]
	res -= (cut << [0, -hbar_offset_y + bar.width/2 - 1, 0]) / [0, 0, -30]

	#### screws
	if bottom:
		res -= screws(bar.width/2)
		res -= screws(h - bar.width/2)
	else:
		res -= screws(h/2)

	res -= z_screws(vbar_screw_distance)
	res -= z_screws(h2 - vbar_screw_distance)
	
	if ends_disks_r:
		disk = cylinder(ends_disks_h, ends_disks_r)
		res += disk << [-bar.width/2, bar.width/2, 0]
		res += disk << [-bar.width/2, -bar.width/2, 0]
		res += (disk << [hbar_offset_x, hbar_offset_y + bar.width/2, 0]) / [0, 0, 30]
		res += (disk << [hbar_offset_x, -hbar_offset_y - bar.width/2, 0]) / [0, 0, -30]
		disk2 = disk << [hbar_mount_len + hbar_offset_x - thickness, 0, 0]
		res += (disk2 << [0, hbar_offset_y - bar.width/2 - thickness/2, 0]) / [0, 0, 30]
		res += (disk2 << [0, -hbar_offset_y + bar.width/2 + thickness/2, 0]) / [0, 0, -30]
		
	return color(config.plcol) (res)

def create_cap():
	x = bar.width/2 + rail.belt_dx
	
	vert = cube([bar.width, bar.width + thickness * 2, cap_t]) << [-bar.width/2, -bar.width/2 - thickness, 0]

	edge = cube([hbar_mount_len, bar.width, cap_t]) << [hbar_offset_x - 0.01, -bar.width/2, 0]
	edge1 = (edge << [0, hbar_offset_y, 0]) / [0, 0, 30]
	edge2 = (edge << [0, -hbar_offset_y, 0]) / [0, 0, -30]

	res = hull() (vert, edge1, edge2)
	
	res -= idler.knob_nut.hole(thickness + 2, 0) << [x, 0, thickness + 1]
	
	res -= idler.create_trigger(gap = True) << [x, 0, 0]

	l = idler.h*2 + idler.cap_gap*2 + idler_slot_t*2
	w = idler.w + idler.cap_gap*2 + idler_slot_t*2
	idler_slot = cube([l, w, idler_slot_h]) << [-l/2 + x, -w/2, cap_t - 0.01]
	idler_slot -= cube([l - idler_slot_t*2, w - idler_slot_t*2, idler_slot_h + 2]) << [-l/2 + idler_slot_t + x, -w/2 + idler_slot_t, cap_t - 1]
	
	res += idler_slot
	
	res -= (screw.m8.hole(cap_t + 2, 0) / [180, 0, 0]) << [0, 0, -1]
	
	scrw = (screw.m5.contersum_hole(cap_t + 2, 3, 9.4, cap_t) / [180, 0, 0]) << [0, 0, 2.75]
	scrws = scrw << [hbar_screw_x1 + hbar_offset_x, 0, 0]
	scrws += scrw << [hbar_screw_x2 + hbar_offset_x, 0, 0]
	
	res -= (scrws << [0, hbar_offset_y, 0]) / [0, 0, 30]
	res -= (scrws << [0, -hbar_offset_y, 0]) / [0, 0, -30]
	
	#res -= cube([200, 200, 200]) << [45, -100, -100]
	
	return color(config.plcol) (res)

def create_modifiers(h):
	mod = cube([bar.width, bar.width, h + 2]) << [-bar.width/2, 0, -1]
	res = mod << [0, bar.width/2 + thickness, 0]
	res += mod << [0, -bar.width * 1.5 - thickness, 0]
	return res