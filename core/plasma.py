import math

from interfaces.iplasma import IPlasma

class PlasmaModule(IPlasma):
    def __init__(self, fabric, nPlasma, R, r, zoom):
        self.set_plasma(nPlasma, R, r, zoom)
        self.set_center(fabric)

    def set_plasma(self, nPlasma, R, r, zoom):
        self._NPLASMA = nPlasma
        self._RPM = None
        self._RAD_M = None
        self._ROTATION = 0
        self._CONVEYOR_SPEED = None
        self._ZOOM = zoom
        self._R = int(R * self._ZOOM)
        self._r = int(r * self._ZOOM)

    def set_center(self, fabric):
        self._CENTER_ORIGIN = [int(fabric / 2), int(fabric / 2)]
        self._CENTER = [int(fabric / 2), int(fabric / 2)]

    def set_radian_per_minute(self, rpm):
        self._RPM = rpm
        self._RAD_M = int(rpm * 360)
        # self.RAD_M_ = int(rpm * 2 * math.pi)

    def set_conveyor_speed_per_minute(self, conveyor_speed_m):
        self._CONVEYOR_SPEED = int(conveyor_speed_m * self._ZOOM)

    def clear_all(self):
        self._CENTER = self._CENTER_ORIGIN
        self._ROTATION = 0

    def update_rotation(self, split):
        self._ROTATION = (self._ROTATION + (self._RAD_M / split)) % 360
        print(self._ROTATION)

    def rotate_plasma(self):
        total_a = []
        total_b = []

        for theta in range(0, 360, int(360 / self._NPLASMA)):
            a = int(self._CENTER[0] + self._R * math.cos(math.radians(theta + self._ROTATION)))
            b = int(self._CENTER[1] + self._R * math.sin(math.radians(theta + self._ROTATION)))

            total_a.append(a)
            total_b.append(b)

        return total_a, total_b, self._r

    def move_center(self, color=(255, 255, 255), thickness=-1, split=1000):
        """ self.CONVEYOR_SPEED_ == 0 이면 예외처리 """
        self._CENTER[0] += (self._CONVEYOR_SPEED / split)

    def next(self, split):
        self.move_center(split=split)
        self.update_rotation(split=split)

        return self.rotate_plasma()


if __name__ == "__main__":

    nPlasma = 10

    fabric = 2000  # mm
    R = 130  # mm
    r = 1.5  # mm
    conveyorSpeed = 5000 * 2  # mm/min
    zoom = 10

    rpm = 333  # round/min

    pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
    pm.set_radian_per_minute(rpm)
    pm.set_conveyor_speed_per_minute(conveyorSpeed)
    print(pm.next(split=int(1024*2)))

