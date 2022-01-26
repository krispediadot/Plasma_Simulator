import numpy as np
import cv2
import math
import os
import datetime

from interfaces.ipalette import IPalette
from core.plasma import PlasmaModule

class Palette(IPalette):
    def __init__(self, fabric, path):
        self.set_palette(fabric, path)

    def set_plasma(self, plasma, rpm, conveyor_speed_m):
        self._PLASMA = plasma
        self._PLASMA.set_center(self._FABRIC)
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
            cv2.imwrite(os.path.join(self._SAVE_PATH, str(datetime.datetime.today())) + '.jpg', self._PALETTE)
            print('[*] saved!')

    def generate_palette_video(self, path):
        """ 수정해야함. """
        pass
        # frame_array = []
        # for filename in os.listdir(path):
        #     if (filename.endswith('.jpg')):
        #         print(filename)
        #         img = cv2.imread(os.path.join(self._SAVE_PATH, filename))
        #         scale_percent = 80
        #
        #         height = int(img.shape[0] * (scale_percent / 100))
        #         width = int(img.shape[1] * (scale_percent / 100))
        #         # layers = img.shape[2] * (scale_percent / 100)
        #
        #         size = (width, height)
        #
        #         img = cv2.resize(img, size)
        #         # height, width, layers = img.shape
        #         # size = (width, height)
        #         frame_array.append(img)
        #
        # print(len(frame_array))
        #
        # out = cv2.VideoWriter(os.path.join(self._SAVE_PATH, f'simulation_{self._RPM}_{self._CONVEYOR_SPEED}.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
        #
        # for i in range(len(frame_array)):
        #     out.write(frame_array[i])
        # out.release()

    def simulation(self, rpm=None, conveyor_speed_m=None, duration_m=None, save=False, imshow=False):

        if (rpm != None and conveyor_speed_m != None):
            self.set_plasma(PlasmaModule(fabric=2000, nPlasma=10, R=130, r=1.5, zoom=10), rpm=rpm, conveyor_speed_m=conveyor_speed_m)
            self.draw_plasma()
            self.generate_palette_image(imshow=imshow)

            for t in range(0, duration_m):
                split = 1024*2 # rpm에 반비례하게 값을 정해줘야할듯

                for i in range(0, split):
                    self.draw_plasma(split=split)
                    if (i%100 == 0):
                        self.generate_palette_image(save=save, imshow=imshow)

        # self.generatePaletteImage()
        # self.generate_palette_video(self._SAVE_PATH)

if __name__ == "__main__" :
    path = '/Users/sujinlee/PycharmProjects/plasma/for_vid'
    P = Palette(fabric=2000, path=path)
    P.simulation(rpm=120, conveyor_speed_m=1000, duration_m=10, imshow=True)