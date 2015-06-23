from opyscad import *
from config import *
import math


class Screw:
	def __init__(self, d1, d2, hole_gap):
		self.d1 = d1
		self.d2 = d2
		self.hole_gap = hole_gap

	def hole(self, h1, h2):
		res = cylinder(h1 + 0.01, d = self.d1 + self.hole_gap, fn = 32)
		res <<= [0, 0, -h1]
		res += cylinder(h2, d = self.d2, fn = 32)
		return res




