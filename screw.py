from opyscad import *
from config import *
import math


class Screw:
	def __init__(self, d, size, gap_thread, gap_octo, gap_cyl):
		self.d = d
		self.size = size
		self.gap_thread = gap_thread
		self.gap_octo = gap_octo
		self.gap_cyl = gap_cyl

	def hole(self, h1, h2, octo = False):
		res = cylinder(h1 + 0.01, d = self.d + self.gap_thread * 2, fn = 32)
		res <<= [0, 0, -h1]
		d_head = self.size * 2 / math.sqrt(3)
		d_head += (self.gap_octo if octo else self.gap_cyl) * 2
		res += cylinder(h2, d = d_head, fn = 6 if octo else 32)
		return res
	
		




