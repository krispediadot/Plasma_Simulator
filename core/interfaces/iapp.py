from abc import *
from core.interfaces.ipalette import IPalette

class IApp(metaclass=ABCMeta):

    @abstractmethod
    def set_palette(self, palette:IPalette):
        """
        connect plasma modules interface
        """
        pass

    @abstractmethod
    def set_style(self):
        """
        define simulator style (color, size, location, flags)
        """
        pass

    @abstractmethod
    def set_window(self, window):
        """
        :param window: gui palette (ex. tkinter.Tk)

        define window design (inputs, buttons, output canvas)
            Inputs
                - rpm
                - conveyor speed(mm/min)
            Buttons
                - result: run simulator
                - stop: stop showing result
                - clear: clear result
            Output Canvas
                - show result images
        """
        pass

    @abstractmethod
    def warn_save_path(self):
        """
        define warning message box for save path
        """
        pass

    @abstractmethod
    def warn_digit(self):
        """
        define waring message box for not digit input types
        """
        pass

    @abstractmethod
    def run_result(self):
        """
        define a method for 'Result' button on GUI
        """
        pass

    @abstractmethod
    def run_stop(self):
        """
        define a method for 'Stop' button on GUI
        """
        pass

    @abstractmethod
    def run_clear(self):
        """
        define a method for 'Clear' button on GUI
        """
        pass