from opyscad import *
import bar, config, screw, motor, rail
import math


thickness = 4.5
hbar_mount_len = 80.0
hbar_offset_x = 30.0 #27
hbar_offset_y = 23.0 #20
hbar_end_screws = False
window_r = 5.0
top_extra_height = 20.0
hbar_screw_type = screw.m5
vbar_screw_type = screw.m5
screw_cap_depth = 1.0
hbar_screw_x1 = 12.0
hbar_screw_x2 = 65.0
vbar_screw_distance = 7.0

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
	scr = hbar_screw_type.hole(thickness + 2, thickness + 2) / [90 * side, 0, 0]
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
	y = (-bar.width/2 - thickness - bar.gap) * side
	return scr << [0, y, z]

def z_screws(z):
	res = z_screw(z, 1)
	res += z_screw(z, -1)
	return res

def create(h, bottom = False, extra_height = 0):
	h2 = h + extra_height
	vert = cube([bar.width, bar.width + thickness * 2, h2]) << [-bar.width/2, -bar.width/2 - thickness, 0]

	edge = cube([hbar_mount_len, bar.width, h]) << [hbar_offset_x - 0.01, -bar.width/2, 0]
	edge1 = (edge << [0, hbar_offset_y, 0]) / [0, 0, 30]
	edge2 = (edge << [0, -hbar_offset_y, 0]) / [0, 0, -30]

	res = hull() (vert, edge1, edge2)

	vert = cube([bar.width + 1, bar.width + bar.gap*2, h2 + 2])
	res -= vert << [-bar.width/2 - 1, -bar.width/2 - bar.gap, -1]

	#### cut edge profile
	edge = cube([hbar_mount_len, bar.width + 1, h2 + 2]) << [hbar_offset_x, -bar.width/2, -1]
	res -= (edge << [0, hbar_offset_y, 0]) / [0, 0, 30]
	res -= (edge << [0, -hbar_offset_y - 1, 0]) / [0, 0, -30]

	#### windows
	y = -hbar_offset_y + bar.width/2 + window_r + thickness
	mx = 1.0/(math.cos(math.pi/6))

	motor_x = bar.width/2 + rail.belt_dx + motor.pulley_dx

	x1 = (bar.width/2 + window_r + thickness) * mx
	x2 = (motor_x - thickness - window_r) * mx

	res -= trapeze(h2 + 2, window_r, x1, x2, y) << [0, 0, -1]

	x1 = (motor_x + window_r)*mx
	x2 = hbar_mount_len + hbar_offset_x
	res -= trapeze(h2 + 2, window_r, x1, x2, y) << [0, 0, -1]

	if bottom:
		cut = cylinder(h = thickness + 2, d = motor.lip_cutout_d, fn = 32) / [0, 90, 0]
		res -= cut << [motor_x - thickness - 1, 0, motor.dz]

		cut = motor.screw.hole(thickness + 1, 2) / [0, -90, 0]
		cut <<= [motor_x - thickness + 1, 0, motor.dz]

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

	return color(config.plcol) (res)

