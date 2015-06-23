#!/usr/bin/python
# -*- coding: utf-8 -*-


from opyscad import *
from config import *
from profile import profile
import math

#TODO сделать безрезьбовую часть у тболта и болта

tslot_height = 6.5
width = 16.75
w_gap = 0.05
diag_gap = 0.2
d_gap = 0
w2_gap = 0.15
nut_gap = 0.1
support = 0.4

### M5 nut
nut_height = 5.0
nut_size = 8.4
nut_hole_d = 5.4


def tslot(length):
	w = width - w_gap * 2
	cut = cube([length + 2, 20, 10]) << [-length/2 - 1, -10, 0]
	res = cube([length, w, tslot_height]) << [-length/2, -w/2, 0]
	res -= (cut / [-45, 0, 0]) << [0, 9.4, 5]
	res -= (cut / [45, 0, 0]) << [0, -9.4, 5]
	res -= (cut / [-45, 0, 0]) << [0, -13.7 + diag_gap, -5]
	res -= (cut / [45, 0, 0]) << [0, 13.7 - diag_gap, -5]
	
	res = (res / [180, 0, 0]) << [0, 0, tslot_height]
	
	return res

def tnut(length, nut, t):
	d = nut_size * 2 / math.sqrt(3)
	res = tslot(length)
	
	res -= nut.hole(t + 1, 20, True) << [0, 0, t]
	#res -= cube([2,2,2]) << [3.7,1,6]
	return res

if __name__ == '__main__':
	tnut(12, m3, 1).save('tnut.scad')
	
