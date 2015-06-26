#!/usr/bin/python


from opyscad import *
import vertex
import config


def create():
	return vertex.create(config.bottom_height, bottom = True)


if __name__ == '__main__':
	res = create()
	res.save('scad/bottom_vertex.scad')
