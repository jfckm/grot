import bmp, prep, tools, solver, postpro

t = tools.timer()

im = bmp.open("im.bmp")
geom = bmp.create_geom(im)

nodes = geom[0].store()
eles = geom[1].store()
c = geom[2]
bc_dict = geom[3]

m = prep.materials(eles)
m.add("steel")
m.assignall(1)
m.set_unit("mm")
#m.set_scale(1)

h = prep.thicks(eles)
h.add(1)
h.assignall(1)

c.load(bc_dict["magenta"], x = 1e2, y = 0)
cons = c.store()

sol = solver.build(nodes, eles, cons)
disp = sol.least_squares()
strains = sol.strains_calc(disp)

post = postpro.prepare(nodes, eles, disp)
post.save_dresults("disp_x")
post.save_dresults("disp_y")
post.save_dresults("disp_mag")

post2 = postpro.prepare(nodes, eles, strains)
post2.save_sresults("eps_x")
post2.save_sresults("eps_y")
post2.save_sresults("gamma_xy")
post2.save_sresults("sig_x")
post2.save_sresults("sig_y")
post2.save_sresults("tau_xy")
post2.save_sresults("huber")

print("")
print("Task finished in", t.check())

"""
bmp im.bmp
mat steel all
unit mm
scale 5
th 2 all
load x 1e4 y 0 magenta
solv direct
res dis m
res str hub
"""