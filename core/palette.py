import numpy as np
import cv2
import math
import os

from core.interfaces.ipalette import IPalette
from core.plasma import PlasmaModule
from core.pipeline import Pipeline
from core.worker import Workers

class Palette(IPalette):

    pipeline = Pipeline()
    worker = Workers()

    _nPlasma = None
    _R = None
    _r = None
    _ZOOM = None
    _PLASMA = None
    _SAVE_PATH = None
    _FABRIC = None
    _PALETTE = None
    _WHITE = None

    def __init__(self, fabric, path):
        self.set_palette(fabric, path)
        self.set_plasma_info()

    def set_plasma_info(self):
        self._nPlasma = 10
        self._R = 130
        self._r = 1.5
        self._ZOOM = 5

    def set_plasma(self, plasma, rpm, conveyor_speed_m):
        self._PLASMA = plasma
        self._PLASMA.set_radian_per_minute(rpm)
        self._PLASMA.set_conveyor_speed_per_minute(conveyor_speed_m)

    def set_palette(self, fabric, path):
        self._SAVE_PATH = path
        self._FABRIC = fabric + 1000
        self._PALETTE = np.zeros((self._FABRIC, int(self._FABRIC * math.pi), 3), np.uint8)
        self._WHITE = (255, 255, 255)

    def clear_palette(self):
        self._PALETTE = np.zeros((self._FABRIC, int(self._FABRIC * math.pi), 3), np.uint8)

    def draw_plasma(self, color=(255, 255, 255), thickness=-1, split=1000):
        total_a, total_b, r = self._PLASMA.next(split)

        for a, b in zip(total_a, total_b):
            self._PALETTE = cv2.circle(self._PALETTE, (a, b), r, self._WHITE, -1)

    def generate_palette_image(self, save=False, imshow=False):
        """ show self.PALETTE """
        if imshow == True:
            cv2.imshow('circle', self._PALETTE)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        if save == True:
            if (os.path.exists(self._SAVE_PATH) == False):
                os.mkdir(self._SAVE_PATH)
            while (self.pipeline.save_idx < len(self.pipeline.queue)):
                cv2.imwrite(os.path.join(self._SAVE_PATH, str(self.pipeline.save_idx)) + '.jpg', self.pipeline.queue[self.pipeline.save_idx])
                self.pipeline.save_idx += 1
            print('[*] saved!')

    def simulation(self, rpm=None, conveyor_speed_m=None, duration_m=None, save=False, imshow=False):

        if (rpm != None and conveyor_speed_m != None):
            center = [int(self._FABRIC / 2), int(self._FABRIC / 2)]
            self.set_plasma(PlasmaModule(center=center, nPlasma=self._nPlasma, R=self._R, r=self._r, zoom=self._ZOOM), rpm=rpm, conveyor_speed_m=conveyor_speed_m)
            self.draw_plasma()
            self.generate_palette_image(imshow=imshow)

            for t in range(0, duration_m):
                split = 1024*2 # rpm에 반비례하게 값을 정해줘야할듯

                for i in range(1, split):
                    self.draw_plasma(split=split)
                    if (i%10 == 0):
                        self.generate_palette_image(save=False, imshow=imshow)
                        self.worker.cv.acquire()
                        self.pipeline.push(self._PALETTE.copy())
                        self.worker.cv.notify()
                        self.worker.cv.release()
                    # if (i%100 == 0):
                    #     self.generate_palette_image(save=True, imshow=False)
                        # self.pipeline.push(self._PALETTE)
                        # print(self.pipeline.print())


        # self.generatePaletteImage()
        # self.generate_palette_video(self._SAVE_PATH)q

if __name__ == "__main__" :
    path = '/Users/sujinlee/PycharmProjects/plasma/for_vid'
    P = Palette(fabric=2000, path=path)
    P.simulation(rpm=120, conveyor_speed_m=500, duration_m=10, imshow=True)