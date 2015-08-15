#!/usr/bin/python
# -*- coding: utf-8 -*-


from opyscad import *
import config, bed, vertex, screw


height = bed.bar2bed_h
length = 100.0
bed_mount_dy = 43.0
bed_mount_dx = bed.l - bed.hole_dx
screw = screw.m3
hole_l = 6.0
bed_hole_dx = 10.0
bar_hole_dx = 10.0

nut_depth = 2.75


def create():
	bar_mount_dx = vertex.base_center2edge() + vertex.hbar_offset_y
	
	width = bar_mount_dx - bed_mount_dx + bed_hole_dx + bar_hole_dx
	res = cube([width, length, height]) << [-bed_hole_dx, -length/2, 0]
	
	cut = screw.hole(height + 1, nut_depth + 1, octo = True) / [180, 0, 0]
	res -= cut << [0, bed_mount_dy, nut_depth]
	res -= cut << [0, -bed_mount_dy, nut_depth]
	
	sup = screw.z_sup(nut_depth + 0.1) / [180, 0, 0]
	res += sup << [0, bed_mount_dy, nut_depth + 0.1]
	res += sup << [0, -bed_mount_dy, nut_depth + 0.1]
	
	cut = screw.hole(height + 1, nut_depth + 1) << [bar_mount_dx - bed_mount_dx, 0, height - nut_depth]
	res -= cut << [0, bed_mount_dy, 0]
	res -= cut << [0, -bed_mount_dy, 0]
	
	return res


if __name__ == '__main__':
	create().save('scad/bed_mount.scad')
	
	