#!/usr/bin/python


from opyscad import *


#### rail
Hr = 8.0
Wr = 12.0
D = 6.0
h = 4.5
d = 3.5
P = 25.0
E = 10.0

#### block
W = 27.0
B = 20.0
B1 = 3.5
C = 20.0
L1 = 32.4
L = 45.4
H2 = 2.5
s_d = 3
s_h = 4

#### assembly
H = 13.0
H1 = 4.0
N = 8.5


def MGN_12H_rail(length):
	res = cube([Hr, Wr, length]) << [0, -Wr/2, 0]
	return res

def MGN_12H_block():
	res = color([0.1, 0.8, 0]) (cube([H - H1, W, L]))

	screw = cylinder(s_h + 1, d = s_d) / [0, 90, 0]
	screw <<= [H - H1 - s_h, 0, 0]

	C1 = (L - C)/2
	res -= screw << [0, B1, C1]
	res -= screw << [0, B1, C1 + C]
	res -= screw << [0, B1 + B, C1]
	res -= screw << [0, B1 + B, C1 + C]


	res <<= [H1, -W/2, -L/2]

	car = color([1, 0.5, 0]) (imp('carriage.stl')) / [90, 0, 90]
	res += car << [H, 0, 0]

	return res
