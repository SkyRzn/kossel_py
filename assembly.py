#!/usr/bin/python


from opyscad import *
from config import *
from vertex import vertex
import math


d = edge_full_len/2/math.cos(math.pi/6)
d2 = edge_full_len*math.cos(math.pi/6) - d


vert = vertex(30) << [-d, 0, 0]

v_edge = cube([profile_w, profile_w, height]) << [-profile_w/2, -profile_w/2, 0]
v_edge <<= [-d, 0, 0]

res = (vert + v_edge)
res += (vert + v_edge) / [0, 0, 120]
res += (vert + v_edge) / [0, 0, -120]

edge = cube([edge_len, profile_w, profile_w])
edge <<= [-edge_len/2, -profile_w/2 - d2 - edge_offset_y-0.1, 0]

res += edge / [0, 0, -30]
res += edge / [0, 0, 90]
res += edge / [0, 0, 210]

res.save('assembly.scad')
