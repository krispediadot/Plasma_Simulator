import threading
import os
import cv2
import datetime
import tkinter
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox as msgbox
from tkinter.filedialog import askdirectory

from PIL import ImageTk, Image

from interfaces.iapp import IApp
from core.palette import Palette
from core.pipeline import Pipeline
from core.worker import Workers

class MainWindow(IApp):

    pipeline = Pipeline()
    worker = Workers()

    _PALETTE = None
    _COLOR_BG = None
    _COLOR_FG = None
    _HEIGHT = None
    _WIDTH = None
    _START_R = None
    _START_C = None
    _PARAMETER_Y_1st = None
    _PARAMETER_Y_2nd = None
    _PARAMETER_Y_3rd = None
    _STOP = None
    _DONE = None
    _BASE_PATH = None
    _WINDOW = None

    _RPM = None
    _CONVEYOR = None

    def __init__(self, window:tkinter.Tk):
        """
        :param window: tkinter.TK
        """
        self.set_style()
        self.set_window(window)

    def set_palette(self, palette):
        self._PALETTE = palette

    def set_style(self):
        """
        define simulator style

        self._COLOR_BG: simulator background color(hex code)
        self._COLOR_FG: simulator foreground color(hex code)
        self._HEIGHT: simulator window height
        self._WIDTH: simulator window width
        self._START_R: simulator pop initial location(row)
        self._START_C: simulator pop initial location(column)
        self._PARAMETER_Y: input labels location(row)
        self._STOP: stop button flag(if True, freeze)
        self._DONE: show result flag(if True, show result on Output Canvas)
        """
        # === Style ===
        self._COLOR_BG = "#565656"
        self._COLOR_FG = "#d3d3d3"
        # fontStyle = tkFont.Font(family="Courier", size=40)
        self._HEIGHT = 500
        self._WIDTH = 1000
        self._START_R = 100
        self._START_C = 200
        self._PARAMETER_Y_1st = 30
        self._PARAMETER_Y_2nd = 90
        self._PARAMETER_Y_3rd = 455
        self._STOP = False
        self._DONE = False

    def set_window(self, window:tkinter.Tk):
        """
        define window design

        Inputs
            - rpm
            - conveyor speed(mm/min)
        Buttons
            - result: run simulator
            - stop: stop showing result
            - clear: clear result
        Output
            - show result images
        """

        self._WINDOW = window

        # == Frame
        self._WINDOW.title("Simulator")
        self._WINDOW.geometry(f"{self._WIDTH}x{self._HEIGHT}+{self._START_R}+{self._START_C}")  # CxR+시작c+시작r
        self._WINDOW.resizable(False, False)
        self._WINDOW.config(bg=self._COLOR_BG)

        # == Inputs
        Label(window, text="RPM", font=("Courier", 20, "normal"), bg=self._COLOR_BG, fg=self._COLOR_FG).place(x=100,
                                                                                                              y=self._PARAMETER_Y_1st,
                                                                                                              anchor='n')
        self.rpm_input = Entry(window, width=10)
        self.rpm_input.place(x=200, y=self._PARAMETER_Y_1st, anchor='n')

        Label(window, text="CONVEYOR", font=("Courier", 20, "normal"), bg=self._COLOR_BG, fg=self._COLOR_FG).place(x=350,
                                                                                                                   y=self._PARAMETER_Y_1st,
                                                                                                                   anchor='n')
        self.conveyor_input = Entry(window, width=10)
        self.conveyor_input.place(x=500, y=self._PARAMETER_Y_1st, anchor='n')

        # == Buttons
        self.btnResult = Button(window, text="Result", command=self.run_result, bg=self._COLOR_FG, fg=self._COLOR_BG)
        self.btnResult.place(x=600, y=self._PARAMETER_Y_1st, anchor='n')

        self.btnStop = Button(window, text="Stop", command=self.run_stop, bg=self._COLOR_FG, fg=self._COLOR_BG)
        self.btnStop.place(x=700, y=self._PARAMETER_Y_1st, anchor='n')

        self.btnClear = Button(window, text="Clear", command=self.run_clear, bg=self._COLOR_FG, fg=self._COLOR_BG)
        self.btnClear.place(x=800, y=self._PARAMETER_Y_1st, anchor='n')

        self.btnSave = Button(window, text="Save", command=self.run_save, bg=self._COLOR_FG, fg=self._COLOR_BG)
        self.btnSave.place(x=900, y=self._PARAMETER_Y_1st, anchor='n')

        # == Outputs
        self.canvas = Canvas(window, width=900, height=350, relief="solid", bd=2)
        # canvas.create_image(455, 5, image=image, anchor='n')
        self.canvas.place(x=500, y=self._PARAMETER_Y_2nd, anchor='n')

        self.result_images = []
        self.image_on_canvas = self.canvas.create_image(455, 5, image=None, anchor='n')
        self.image = None

        # == Signiture
        path = '/Users/sujinlee/PycharmProjects/plasma/signiture_.png'
        img = Image.open(path)
        self.img_signiture = ImageTk.PhotoImage(img.resize((240, 42)))
        print(self.img_signiture)
        Label(window, image=self.img_signiture).place(x=500, y=self._PARAMETER_Y_3rd, anchor='n')

    def warn_save_path(self):
        msgbox.showwarning("Warning", "저장 위치를 지정해주세요!")

    def warn_digit(self):
        msgbox.showwarning("Warning", "숫자를 입력해주세요!")

    def run_simulation(self, rpm, conveyor, path):
        print("simulation start")
        self.set_palette(Palette(fabric=2000, path=path))
        # self._PALETTE.simulation(rpm=rpm, conveyor_speed_m=conveyor, duration_m=10, save=True, imshow=False)

        producer_th = threading.Thread(target=self._PALETTE.simulation, args=(rpm, conveyor, 1))
        consumer_th = threading.Thread(target=self.show)

        producer_th.start()
        consumer_th.start()

        self._DONE = True

    def run_result(self):
        """
        run simulator
        """

        # == Inputs
        self._RPM = self.rpm_input.get()
        print(self._RPM)
        self.rpm_input.delete(0, END)

        self._CONVEYOR = self.conveyor_input.get()
        print(self._CONVEYOR)
        self.conveyor_input.delete(0, END)

        # 추후 입력 받도록 수정 필요.
        self._BASE_PATH = '/Users/sujinlee/PycharmProjects/plasma/results'

        # = check
        if self._RPM.isdigit() == False or self._CONVEYOR.isdigit() == False:
            self.warn_digit()
            return

        save_path = f'{self._BASE_PATH}/{self._RPM}_{self._CONVEYOR}'

        if os.path.exists(save_path) == False:
            os.mkdir(save_path)
            self.run_simulation(int(self._RPM), int(self._CONVEYOR), save_path)
        else:
            self._DONE = True
            self.show_result(save_path)

        # if self._DONE == True:
        #     self.show_result(save_path)

    def run_stop(self):
        print('STOP')
        self._STOP = not self._STOP

    def run_clear(self):
        print('CLEAR')
        self.image = None
        self._STOP = False
        self._DONE = False
        self.pipeline.queue = []
        self.pipeline.show_idx = 0
        self.cv = threading.Condition()
        self.done = False

    def run_save(self):
        self._BASE_PATH = askdirectory(initialdir='./',
                                       # filetypes=[("PNG", "*.png"),
                                       #            ("JPG", "*.jpg")],
                                       title='Choose a path.')
        print('Path to File: \n', self._BASE_PATH)

        if (os.path.exists(self._BASE_PATH) == False):
            os.mkdir(self._BASE_PATH)
        cv2.imwrite(os.path.join(self._BASE_PATH, str(datetime.datetime.today())) + '.jpg', self.pipeline.queue[self.pipeline.show_idx])
        print('[*] saved!')

    def show(self):
        while (self._STOP == False):
            self.worker.cv.acquire()

            while (len(self.pipeline.queue) <= self.pipeline.show_idx):
                print('consumer waiting...')
                self.worker.cv.wait()

            img_new = Image.fromarray(self.pipeline.queue[self.pipeline.show_idx])
            print(img_new)
            self.pipeline.show_idx += 1
            self.image = ImageTk.PhotoImage(img_new.resize((900, 350)))
            self.canvas.itemconfig(self.image_on_canvas, image=self.image)
            self._WINDOW.update()
            self.worker.cv.release()


    def show_result(self, path):
        """
        open result images & display the images on simulator
        """
        # 병렬로 수정해야함.
        # 현재는 이미지를 모두 읽어와서 큐에서 빼내는 방식으로 구현되어 있음.
        for file in os.listdir(path):
            if file.endswith('.jpg'):
                self.result_images.append(os.path.join(path, file))
                print(file)

        self.result_images.sort()

        while len(self.result_images) > 0:
            if self._STOP == True:
                self.result_images = []
                break

            img_new = Image.open(self.result_images[0])
            print(type(self.result_images[0]))
            print(img_new)
            self.result_images.pop(0)
            self.image = ImageTk.PhotoImage(img_new.resize((900, 350)))
            self.canvas.itemconfig(self.image_on_canvas, image=self.image)
            self._WINDOW.update()
            # time.sleep(0.005)

    def generate_video(self):
        pass


if __name__ == "__main__":
    window = Tk()
    MainWindow(window)
    window.mainloop()