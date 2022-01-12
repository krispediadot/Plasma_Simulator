from plasma import PlasmaModule

import math

nPlasma = 10

fabric = 2000 #mm
R = 130 #mm
r = 1.5 #mm
conveyorSpeed = 5000 #mm/min
zoom = 8

rpm = 100 #round/min
rad_m = int(rpm*math.pi)

pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
# pm.simulation(rpm=100, duration_m=3)
# pm.simulation(conveyorSpeed_m=5000, duration_m=5)
# pm.clearAll()
# pm.simulation()
pm.simulation(rpm=100, conveyorSpeed_m=5, duration_m=100)

print(pm.CENTER_)
print(pm.ROTATION_)