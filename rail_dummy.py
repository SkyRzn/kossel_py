#!/usr/bin/python
# -*- coding: utf-8 -*-


from opyscad import *
import screw
import math


height = 10.0
width = 14.0
length = 10.0
t = 3.0


def dummy():
	res = cube([length, width, height]) << [-length/2, -width/2, 0]
	res -= screw.m3.hole(t + 1, height) << [0, 0, t]
	
	return res

if __name__ == '__main__':
	dummy().save('scad/rail_dummy.scad')
	
