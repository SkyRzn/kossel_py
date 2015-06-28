from opyscad import *
import vertex, config, belt, screw


dz = 35.0
pulley_dx = 16.0
lip_cutout_d = 25.0
screw_dist = 15.5
screw = screw.m3


def create():
	res = imp('../src/nema17.stl') / [0, -90, 0]
	return res



