from opyscad import *
from config import plcol


ext_dz = 30.0
rod_dx = 20.0
rod_dy = 23.0
eff_dz = -4.0


def create(p):
	eff = (color(plcol)(imp('../src/effector.stl')) / [0, 0, 30]) << [0, 0, eff_dz]
	axe = +(cylinder(60, 1.5) / [90, 0, 0]) << [-rod_dx, 30, 0]
	eff += axe
	eff += axe / [0, 0, 120]
	eff += axe / [0, 0, 240]
	res = eff << p
	z = p[2]
	p[2] = 0
	res += +cylinder(z, 0.5) << p

	return res

