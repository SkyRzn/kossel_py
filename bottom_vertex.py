#!/usr/bin/python


from opyscad import *
from vertex import vertex
from config import *


def bottom_vertex():
	return vertex(bottom_h, bottom = True)

if __name__ == '__main__':
	res = bottom_vertex()
	res.save('bottom_vertex.scad')
