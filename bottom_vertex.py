#!/usr/bin/python


from opyscad import *
import vertex
import config


def create(ends_disks_r = 0):
	return vertex.create(config.bottom_height, bottom = True, ends_disks_r = ends_disks_r)


if __name__ == '__main__':
	res = create(8.0)
	res.save('scad/bottom_vertex.scad')
