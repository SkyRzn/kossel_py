from opyscad import *


d = 3.0
D = 10.0
D1 = 11.5
B = 4.0
B1 = 1.0


def create():
	res = cylinder(h = B - 0.1, d = D, fn=32) << [0, 0, 0.1]
	res += cylinder(h = B1, d = D1, fn=32)
	res -= cylinder(h = B + 2, d = d, fn = 16) << [0, 0, -1]
	return res / [0, 90, 0]

def create_couple():
	res = create() << [-B, 0, 0]
	res += (create() / [0, 0, 180]) << [B, 0, 0]
	return res

