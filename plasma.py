import numpy as np
import cv2
import math

import os
import datetime

SAVE_PATH = '/Users/sujinlee/PycharmProjects/plasma/result_img'

class PlasmaModule:
    def __init__(self, fabric, nPlasma, R, r, zoom):

        self.FABRIC_ = fabric*zoom
        self.PALETTE_ = np.zeros((self.FABRIC_, int(self.FABRIC_*math.pi), 3), np.uint8)
        self.CENTER_ORIGIN_ = [int(self.FABRIC_/2), int(self.FABRIC_/2)]
        self.CENTER_ = [int(self.FABRIC_/2), int(self.FABRIC_/2)]

        self.nPlasma_ = nPlasma
        self.ROTATION_ = 0
        self.ZOOM_ = zoom
        self.R_ = int(R*self.ZOOM_)
        self.r_ = int(r*self.ZOOM_)

        self.WHITE_ = (255, 255, 255)

    def clearPalette(self):
        self.PALETTE_ = np.zeros((self.FABRIC_, int(self.FABRIC_ * math.pi), 3), np.uint8)

    def clearAll(self):
        self.CENTER_ = self.CENTER_ORIGIN_
        self.ROTATION_ = 0
        self.PALETTE_ = np.zeros((self.FABRIC_, int(self.FABRIC_ * math.pi), 3), np.uint8)

    def drawPlasma(self, color=(255, 255, 255), thickness=-1):
        # self.PALETTE = cv2.circle(self.PALETTE, (self.CENTER_[0], self.CENTER_[1]), self.R_, color, 0) #plasma module shape

        self.ROTATION_ %= int(360 / self.nPlasma_)

        for theta in range(0, 360, int(360 / self.nPlasma_)):
            a = int(self.CENTER_[0] + self.R_ * math.cos(math.radians(theta + self.ROTATION_)))
            b = int(self.CENTER_[1] + self.R_ * math.sin(math.radians(theta + self.ROTATION_)))

            self.PALETTE_ = cv2.circle(self.PALETTE_, (a, b), self.r_, color, -1)

    def rotatePlasma(self, speed=1, color=(255, 255, 255), thickness=-1):
        """ 수정해야함. for ~ range(----- 이부분) """
        for rotation in range(0, 360, speed):
            self.ROTATION_ = rotation
            self.drawPlasma(color, thickness)

    def moveCenter(self, speed=1, color=(255, 255, 255), thickness=-1):
        """ 수정해야함. for ~ range(----- 이부분) """
        for move in range(0, 1000):
            self.CENTER_[0] += speed
            self.drawPlasma(color, thickness)

    def generatePaletteImage(self):
        """ show self.PALETTE """
        cv2.imshow('circle', self.PALETTE_)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(os.path.join(SAVE_PATH, str(datetime.datetime.today())) + '.jpg', self.PALETTE_)

    def simulation(self, rpm=None, conveyorSpeed=None):
        # self.drawPlasma()
        if (rpm != None):
            self.rotatePlasma(speed=rpm)
        if (conveyorSpeed != None):
            self.moveCenter(speed=conveyorSpeed)
        if (rpm == None and conveyorSpeed == None):
            for move in range(0, 1000):
                self.CENTER_[0] += 5
                for rotation in range(0, 360, 10):
                    self.ROTATION_ = rotation
                    self.drawPlasma()

        self.generatePaletteImage()


if __name__ == "__main__":
    fabric = 2000
    nPlasma = 10
    R = 130
    r = 1.5
    zoom = 4

    pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
    pm.simulation(rpm=1)
    pm.simulation(conveyorSpeed=1)

