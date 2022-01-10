from plasma import PlasmaModule

fabric = 2
nPlasma = 10
R = 0.130
r = 0.0015
zoom = 2000

pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
pm.simulation(rpm=10)
pm.simulation(conveyorSpeed=5)
pm.clearAll()
pm.simulation()

print(pm.CENTER_)
print(pm.ROTATION_)