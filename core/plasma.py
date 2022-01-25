import numpy as np
import cv2
import math

import os
import datetime

class PlasmaModule:
    def __init__(self, fabric, nPlasma, R, r, zoom, save_path):

        self._SAVE_PATH = save_path

        self._FABRIC = fabric + 1000
        self._PALETTE = np.zeros((self._FABRIC, int(self._FABRIC * math.pi), 3), np.uint8)
        self._CENTER_ORIGIN = [int(self._FABRIC / 2), int(self._FABRIC / 2)]
        self._CENTER = [int(self._FABRIC / 2), int(self._FABRIC / 2)]

        self._NPLASMA = nPlasma
        self._RPM = 0
        self._RAD_M = 0
        self._ROTATION = 0
        self._CONVEYOR_SPEED = 0
        self._ZOOM = zoom
        self._R = int(R * self._ZOOM)
        self._r = int(r * self._ZOOM)

        self._WHITE = (255, 255, 255)

        self.totalPlasma = 0

    def set_radian_per_minute(self, rpm):
        self._RPM = rpm
        self._RAD_M = int(rpm * 360)
        # self.RAD_M_ = int(rpm * 2 * math.pi)

    def set_conveyor_speed_per_minute(self, conveyor_speed_m):
        self._CONVEYOR_SPEED = int(conveyor_speed_m * self._ZOOM)

    def clear_palette(self):
        self._PALETTE = np.zeros((self._FABRIC, int(self._FABRIC * math.pi), 3), np.uint8)

    def clear_all(self):
        self._CENTER = self._CENTER_ORIGIN
        self._ROTATION = 0
        self._PALETTE = np.zeros((self._FABRIC, int(self._FABRIC * math.pi), 3), np.uint8)

    def draw_plasma(self, color=(255, 255, 255), thickness=-1):
        # self.PALETTE_ = cv2.circle(self.PALETTE_, (self.CENTER_[0], self.CENTER_[1]), self.R_, color, 0) #plasma module shape
        # self.ROTATION_ %= int(360 / self.nPlasma_)

        for theta in range(0, 360, int(360 / self._NPLASMA)):
            a = int(self._CENTER[0] + self._R * math.cos(math.radians(theta + self._ROTATION)))
            b = int(self._CENTER[1] + self._R * math.sin(math.radians(theta + self._ROTATION)))

            self._PALETTE = cv2.circle(self._PALETTE, (a, b), self._r, color, -1)

        self.totalPlasma += self._NPLASMA

    def rotate_plasma(self, color=(255, 255, 255), thickness=-1, split=1000):
        """ self.ROTATION_ == 0 이면 예외처리"""
        self._ROTATION = (self._ROTATION + (self._RAD_M / split)) % 360
        # self.drawPlasma(color, thickness)

    def move_center(self, color=(255, 255, 255), thickness=-1, split=1000):
        """ self.CONVEYOR_SPEED_ == 0 이면 예외처리 """
        self._CENTER[0] += (self._CONVEYOR_SPEED / split)
        # self.drawPlasma(color, thickness)

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
        frame_array = []
        for filename in os.listdir(path):
            if (filename.endswith('.jpg')):
                print(filename)
                img = cv2.imread(os.path.join(self._SAVE_PATH, filename))
                scale_percent = 80

                height = int(img.shape[0] * (scale_percent / 100))
                width = int(img.shape[1] * (scale_percent / 100))
                # layers = img.shape[2] * (scale_percent / 100)

                size = (width, height)

                img = cv2.resize(img, size)
                # height, width, layers = img.shape
                # size = (width, height)
                frame_array.append(img)

        print(len(frame_array))

        out = cv2.VideoWriter(os.path.join(self._SAVE_PATH, f'simulation_{self._RPM}_{self._CONVEYOR_SPEED}.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 15, size)

        for i in range(len(frame_array)):
            out.write(frame_array[i])
        out.release()

    def simulation(self, rpm=None, conveyor_speed_m=None, duration_m=None, save=False, imshow=False):
        self.draw_plasma()
        self.generate_palette_image()

        if (rpm != None and conveyor_speed_m != None):
            self.set_radian_per_minute(rpm)
            self.set_conveyor_speed_per_minute(conveyor_speed_m)

            for t in range(0, duration_m):
                # split = int(math.pow(2, rpm/10))
                split = 1024

                for i in range(0, split):
                    self.move_center(split=split)
                    self.rotate_plasma(split=split)
                    self.draw_plasma()
                    print(self._ROTATION)
                    if (i%100 == 0):
                        self.generate_palette_image(save=save, imshow=imshow)
                    # if (i % int(split/60) == 0):
                    #     self.generatePaletteImage(save=True)


        print(self.totalPlasma)
        # self.generatePaletteImage()
        self.generate_palette_video(self._SAVE_PATH)


if __name__ == "__main__":
    fabric = 2000
    nPlasma = 10
    R = 130
    r = 1.5
    zoom = 4

    pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
    pm.simulation(rpm=1)
    pm.simulation(conveyorSpeed=1)

