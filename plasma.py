import numpy as np
import cv2
import math

import os
import datetime

SAVE_PATH = '/Users/sujinlee/PycharmProjects/plasma/result_img'

class PlasmaModule:
    def __init__(self, fabric, nPlasma, R, r, zoom):

        # self.FABRIC_ = fabric*zoom
        self.FABRIC_ = fabric + 1000
        self.PALETTE_ = np.zeros((self.FABRIC_, int(self.FABRIC_*math.pi), 3), np.uint8)
        self.CENTER_ORIGIN_ = [int(self.FABRIC_/2), int(self.FABRIC_/2)]
        self.CENTER_ = [int(self.FABRIC_/2), int(self.FABRIC_/2)]

        self.nPlasma_ = nPlasma
        self.RAD_M_ = 0
        self.ROTATION_ = 0
        self.CONVEYOR_SPEED_ = 0
        self.ZOOM_ = zoom
        self.R_ = int(R*self.ZOOM_)
        self.r_ = int(r*self.ZOOM_)

        self.WHITE_ = (255, 255, 255)

        self.totalPlasma = 0

    def setRadianPerMinute(self, rpm):
        self.RAD_M_ = int(rpm*math.pi)

    def setConveyorSpeedPerMinute(self, conveyorSpeed_m):
        self.CONVEYOR_SPEED_ = int(conveyorSpeed_m*self.ZOOM_)

    def clearPalette(self):
        self.PALETTE_ = np.zeros((self.FABRIC_, int(self.FABRIC_ * math.pi), 3), np.uint8)

    def clearAll(self):
        self.CENTER_ = self.CENTER_ORIGIN_
        self.ROTATION_ = 0
        self.PALETTE_ = np.zeros((self.FABRIC_, int(self.FABRIC_ * math.pi), 3), np.uint8)

    def drawPlasma(self, color=(255, 255, 255), thickness=-1):
        # self.PALETTE_ = cv2.circle(self.PALETTE_, (self.CENTER_[0], self.CENTER_[1]), self.R_, color, 0) #plasma module shape

        self.ROTATION_ %= int(360 / self.nPlasma_)

        for theta in range(0, 360, int(360 / self.nPlasma_)):
            a = int(self.CENTER_[0] + self.R_ * math.cos(math.radians(theta + self.ROTATION_)))
            b = int(self.CENTER_[1] + self.R_ * math.sin(math.radians(theta + self.ROTATION_)))

            self.PALETTE_ = cv2.circle(self.PALETTE_, (a, b), self.r_, color, -1)

        self.totalPlasma += self.nPlasma_

    def rotatePlasma(self, color=(255, 255, 255), thickness=-1):
        """ self.ROTATION_ == 0 이면 예외처리"""
        self.ROTATION_ = (self.ROTATION_ + self.RAD_M_) % 360
        # self.drawPlasma(color, thickness)

    def moveCenter(self, color=(255, 255, 255), thickness=-1):
        """ self.CONVEYOR_SPEED_ == 0 이면 예외처리 """
        self.CENTER_[0] += self.CONVEYOR_SPEED_
        # self.drawPlasma(color, thickness)

    def generatePaletteImage(self, save=False):
        """ show self.PALETTE """
        cv2.imshow('circle', self.PALETTE_)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if (save):
            cv2.imwrite(os.path.join(SAVE_PATH, str(datetime.datetime.today())) + '.jpg', self.PALETTE_)
            print('[*] saved!')

    def simulation(self, rpm=None, conveyorSpeed_m=None, duration_m=None):
        self.drawPlasma()
        self.generatePaletteImage()

        # if (rpm != None):
        #     self.setRadianPerMinute(rpm)
        #     print(self.RAD_M_)
        #     for t in range(0, duration_m):
        #         self.rotatePlasma()
        #         self.drawPlasma()
        #
        # if (conveyorSpeed_m != None):
        #     self.setConveyorSpeedPerMinute(conveyorSpeed_m)
        #     print(self.CONVEYOR_SPEED_)
        #     for t in range(0, duration_m):
        #         self.moveCenter()
        #         self.drawPlasma()

        if (rpm != None and conveyorSpeed_m != None):
            self.setRadianPerMinute(rpm)
            self.setConveyorSpeedPerMinute(conveyorSpeed_m)

            for t in range(0, duration_m):
                self.rotatePlasma()
                self.moveCenter()
                self.drawPlasma()
                self.generatePaletteImage(save=True)

        print(self.totalPlasma)
        # self.generatePaletteImage()


if __name__ == "__main__":
    fabric = 2000
    nPlasma = 10
    R = 130
    r = 1.5
    zoom = 4

    pm = PlasmaModule(fabric, nPlasma, R, r, zoom)
    pm.simulation(rpm=1)
    pm.simulation(conveyorSpeed=1)

