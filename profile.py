#!/usr/bin/python


from opyscad import *


def profile(h):
	res = imp('profile.dxf')
	res = linear_extrude(h) (res)
	
	return res

