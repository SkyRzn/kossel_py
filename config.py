
### main
edge_len = 360
height = 750
bottom_h = 70
bed_d = 260
bed_t = 3
bed_h = bottom_h + 2

### profile
profile_w = 30
profile_slot_w = 8
profile_slot_d = 6
profile_gap = 0.2

edge_offset_x = 27
edge_offset_y = 20
edge_profile_len = edge_len - edge_offset_x*2

### vertex
vertex_l = 80
vertex_t = 4

window_r = 6

edge_screw_d1 = 6
edge_screw_d2 = 10
edge_screw_t = 1
edge_screw1_x = 12
edge_screw2_x = 65

edge_full_len = edge_len + edge_offset_x * 2

#### fn
preview = 0

if preview:
	screw_fn = 8
	corner_fn = 8
else:
	screw_fn = 24
	corner_fn = 64



### convert to float
for k, v in locals().items():
	if type(v) == int:
		locals()[k] = float(v)

print 'Full edge len = %.2f' % (edge_full_len)