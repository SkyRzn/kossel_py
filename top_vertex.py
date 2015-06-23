#!/usr/bin/python


from opyscad import *
from vertex import create_vertex
from config import *


def create_top_vertex():
	return create_vertex(bar.width, extra_height = vertex.top_extra_height)

if __name__ == '__main__':
	res = create_top_vertex()
	res.save('top_vertex.scad')
