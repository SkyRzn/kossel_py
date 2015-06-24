from screw import Screw
import math


class Settings():
	def __init__(self):
		for key in dir(self):
			val = getattr(self, key)
			if type(val) == int:
				setattr(self, key, float(val))

m6 = Screw(6, 10, 0.3, 0.3, 0.5)
m5 = Screw(5, 8, 0.3, 0.3, 0.5)
m3 = Screw(3, 5.5, 0.25, 0.4, 0.5)

class Main(Settings):
	hbar_len = 340
	vbar_len = 750
main = Main()

class Bar(Settings):
	width = 30
	slot_width = 8
	slot_depth = 6
	gap = 0.2
bar = Bar()

class Vertex(Settings):
	thickness = 4.5
	hbar_mount_len = 80
	hbar_offset_x = 27
	hbar_offset_y = 20
	hbar_end_screws = True
	window_r = 6
	top_extra_height = 20
	bottom_height = 70
	hbar_screw = m5
	vbar_screw = m5
	screw_cap_depth = 1
	hbar_screw_x1 = 12
	hbar_screw_x2 = 65
	vbar_screw_distance = 6
	def base_edge_len(self):
		return main.hbar_len + self.hbar_offset_x * 2
	def base_center2vertex(self):
		return self.base_edge_len()/2/math.cos(math.pi/6)
	def base_center2edge(self):
		return self.base_edge_len() * math.cos(math.pi/6) - self.base_center2vertex()
vertex = Vertex()

class Rail(Settings):
	length = 600
	z = 100
rail = Rail()

class Bed(Settings):
	diameter = 260
	thickness = 3
	height = vertex.bottom_height + 2
bed = Bed()






