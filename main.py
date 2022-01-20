from core.plasma import PlasmaModule

SAVE_PATH = '/Users/sujinlee/PycharmProjects/plasma/for_vid'

nPlasma = 10

fabric = 2000 #mm
R = 130 #mm
r = 1.5 #mm
conveyorSpeed = 5000*2 #mm/min
zoom = 10

rpm = 333 #round/min

pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
pm.simulation(rpm=rpm, conveyorSpeed_m=conveyorSpeed, duration_m=100)

# pm.generatePaletteVideo(SAVE_PATH)