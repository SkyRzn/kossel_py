#!/usr/bin/python
# -*- coding: utf-8 -*-


from opyscad import *
import screw
import math


tslot_height = 6.5
width = 16.75
w_gap = 0.05
diag_gap = 0.2


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
	res = tslot(length)
	res -= nut.hole(t + 1, 20, True) << [0, 0, t]
	return res

if __name__ == '__main__':
	tnut(12, screw.m3, 1).save('scad/tnut.scad')
	
