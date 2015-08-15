#!/usr/bin/python


from opyscad import *
import vertex, bar


def create(ends_disks_r = 0):
	return vertex.create(bar.width, extra_height = vertex.top_extra_height, ends_disks_r = ends_disks_r)

def create_cap():
	res = vertex.create_cap()
	res <<= [0, 0, -vertex.cap_t]
	return res

if __name__ == '__main__':
	res = create(8.0)
	res.save('scad/top_vertex.scad')
	res = vertex.create_modifiers(bar.width + vertex.top_extra_height)
	res.save('scad/top_vertex_modifiers.scad')
	res = vertex.create_cap()
	res.save('scad/top_vertex_cap.scad')
