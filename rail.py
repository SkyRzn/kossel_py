from opyscad import *
import vertex, config, bar, rod, carriage


length = 600.0
rail_z = 80.0

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
C1 = (L - C)/2

#### assembly
H = 13.0
H1 = 4.0
N = 8.5

rod_mount_dx = H + carriage.rod_dx
belt_dx = H + carriage.belt_dx


def rail(length):
	res = cube([Hr, Wr, length]) << [0, -Wr/2, 0]
	return color(config.railcol) (res)

def block():
	res = color(config.blockcol) (cube([H - H1, W, L]))

	screw = cylinder(s_h + 1, d = s_d) / [0, 90, 0]
	screw <<= [H - H1 - s_h, 0, 0]

	res -= screw << [0, B1, C1]
	res -= screw << [0, B1, C1 + C]
	res -= screw << [0, B1 + B, C1]
	res -= screw << [0, B1 + B, C1 + C]

	res <<= [H1, -W/2, -L/2]

	return res

def create(z):
	rl = rail(length) << [0, 0, rail_z]
	blk = block() << [0, 0, -carriage.rod_dz]
	blk += carriage.create() << [H, 0, 0]
	return rl + (blk << [0, 0, z])

