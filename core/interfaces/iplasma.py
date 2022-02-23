from abc import *

class IPlasma(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, fabric, nPlasma, R, r, zoom):
        pass

    @abstractmethod
    def set_plasma(self, nPlasma, R, r, zoom):
        """
        :param nPlasma: the number of plasma
        :param R: wheel which contains nPlasma R
        :param r: plasma r
        :param zoom: zoom ratio
        """
        pass

    @abstractmethod
    def set_center(self, fabric):
        """
        :param fabric: length of fabric

        define plasma center
        """
        pass

    @abstractmethod
    def set_radian_per_minute(self, rpm):
        pass

    @abstractmethod
    def set_conveyor_speed_per_minute(self, conveyorSpeed_m):
        pass

    @abstractmethod
    def rotate_plasma(self, color=(255, 255, 255), thickness=-1, split=1000):
        pass

    @abstractmethod
    def move_center(self, color=(255, 255, 255), thickness=-1, split=1000):
        pass

    @abstractmethod
    def next(self, split):
        """
        :param split:
        :return: nPlasma's position, self._r

        combine
            - rotate
            - move

        """
        pass

