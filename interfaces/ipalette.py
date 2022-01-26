from abc import *
from interfaces.iplasma import IPlasma

class IPalette(metaclass=ABCMeta):
    """
    draw result on palette
    """

    @abstractmethod
    def set_plasma(self, plasma:IPlasma, rpm, conveyor_speed_m):
        """
        :param plasma: Plasma
        :param rpm: input rpm
        :param conveyor_speed_m: input conveyor_speed_m

        connect plasma
        """
        pass

    @abstractmethod
    def set_palette(self, fabric, path):
        """
        :param fabric: length of fabric
        :param path: save path
        """
        pass

    @abstractmethod
    def clear_palette(self):
        pass

    @abstractmethod
    def draw_plasma(self, color=(255, 255, 255), thickness=-1, split=1024*2):
        pass

    @abstractmethod
    def generate_palette_image(self, save=False):
        pass

    @abstractmethod
    def generate_palette_video(self, imagePath):
        pass

    @abstractmethod
    def simulation(self, rpm=None, conveyorSpeed_m=None, duration_m=None):
        pass