from plasma import PlasmaModule

import math

SAVE_PATH = '/Users/sujinlee/PycharmProjects/plasma/result_img'

nPlasma = 10

fabric = 2000 #mm
R = 130 #mm
r = 1.5 #mm
conveyorSpeed = 5000 #mm/min
zoom = 8

rpm = 100 #round/min

pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
pm.simulation(rpm=100, conveyorSpeed_m=500, duration_m=100)
                                                          