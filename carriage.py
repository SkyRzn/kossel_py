from opyscad import *
from config import plcol
import effector


rod_dx = 6.5
rod_dz = 16.0
rod_dy = effector.rod_dy
belt_dx = 9.5


def create(axe = True):
	res = (color(plcol)(imp('../src/carriage.stl')) / [90, 0, 90]) << [0, 0, -rod_dz]
	res += +(cylinder(60, 1.7) / [90,0,0]) << [rod_dx, 30, 0]
	return res

