#!/usr/bin/python


from opyscad import *
import vertex
import bar


def create():
	return vertex.create(bar.width, extra_height = vertex.top_extra_height)


if __name__ == '__main__':
	res = create()
	res.save('scad/top_vertex.scad')
