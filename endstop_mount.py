from opyscad import *
import screw


l = 30.0
h  = 26.0
t = 4.5

screw_dz = 4.0
screw_head_depth = 3.0
nut_depth = 3.5
nut_dz = 5.0
nut_dx1 = 4.0
nut_dx2 = nut_dx1 + 19.0

lip_h = 1.75
lip_d = 6.0


def create():
	res = cube([l, h, t])
	
	lip = cylinder(lip_h, d=lip_d, fn=32) << [0, nut_dz, t-0.01]
	res += lip << [nut_dx1, 0, 0]
	res += lip << [nut_dx2, 0, 0]
	
	scr = screw.m3.hole(t + 1, screw_head_depth + 1) << [l/2, 0, t - screw_head_depth]
	res -= scr << [0, screw_dz, 0]
	res -= scr << [0, h - screw_dz, 0]
	
	scr = screw.m3.hole(t + 1, nut_depth + 1, octo = True) / [180, 0, 0]
	scr <<= [0, nut_dz, nut_depth]
	res -= scr << [nut_dx1, 0, 0]
	res -= scr << [nut_dx2, 0, 0]
	
	scr = screw.m3.z_sup(nut_depth + 0.01) / [180, 0, 0]
	scr <<= [0, nut_dz, nut_depth]
	res += scr << [nut_dx1, 0, 0]
	res += scr << [nut_dx2, 0, 0]
	
	return res

if 1: #__name__ == '__main__':
	create().save('scad/endstop_mount.scad')
