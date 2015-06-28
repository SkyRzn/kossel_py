from opyscad import *
import math


class Screw:
	def __init__(self, d, size, gap_thread, gap_octo, gap_cyl):
		self.d = d
		self.size = size
		self.gap_thread = gap_thread
		self.gap_octo = gap_octo
		self.gap_cyl = gap_cyl

	def hole(self, h1, h2, h3 = 0, d3 = 0, octo = False):
		d_head = self.size * 2 / math.sqrt(3)
		d_head += (self.gap_octo if octo else self.gap_cyl) * 2
		res = cylinder(h1 + 0.01, d = self.d + self.gap_thread * 2, fn = 32)
		res <<= [0, 0, -h1]
		res += cylinder(h2, d = d_head, fn = 6 if octo else 32)
		if h3 and d3:
			res += cylinder(h3, d = d3, fn = 32) << [0, 0, h2 - 0.01]
		return res
	
	def z_sup(self, h):
		res = cylinder(h + 0.1, d = self.d + self.gap_thread * 2, fn = 16)
		#res -= cylinder(h + 2, d = self.d + self.gap_thread * 2, fn = 16) << [0, 0, -1]
		return res
	
m3 = Screw(3.0, 5.5, 0.25, 0.4, 0.5)
m5 = Screw(5.0, 8.0, 0.3, 0.3, 0.5)
m6 = Screw(6.0, 10.0, 0.3, 0.4, 0.5)
m8 = Screw(8.0, 13.0, 0.5, 0.7, 1)





