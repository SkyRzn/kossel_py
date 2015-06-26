from opyscad import *


width = 30.0
slot_width = 8.0
slot_depth = 6.0
gap = 0.2
profile = '../src/profile.dxf'


def create(h):
	if profile:
		res = imp(profile)
		res = linear_extrude(h) (res)
	else:
		res = cube([width, width, h]) << [-width/2, -width/2, 0]
	return res

