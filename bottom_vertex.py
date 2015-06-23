#!/usr/bin/python


from opyscad import *
from vertex import create_vertex
from config import *


def create_bottom_vertex():
	return create_vertex(vertex.bottom_height, bottom = True)

if __name__ == '__main__':
	res = create_bottom_vertex()
	res.save('bottom_vertex.scad')
