#!/usr/bin/python


from opyscad import *
from vertex import vertex
from config import *


def top_vertex():
	return vertex(profile_w)

if __name__ == '__main__':
	res = top_vertex()
	res.save('top_vertex.scad')
