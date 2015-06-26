from opyscad import *
import vertex, config, bar, rail, motor


D = 10.0
D1 = 15.0
d = 5.0
B1 = 4.0
B2 = 1.0
B = 11.0


def create():
	res = cylinder(h = B - 0.2, d = D) << [0, 0, 0.1]
	res += cylinder(h = B1, d = D1)
	res += cylinder(h = B2, d = D1) << [0, 0, B - B2]
	res -= cylinder(h = B + 2, d = d) << [0, 0, -1]
	res /= [0, -90, 0]
	return res << [B1 + (B - B1 - B2)/2, 0, 0]


