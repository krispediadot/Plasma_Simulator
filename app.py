import os
import time
import tkinter
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox as msgbox

from PIL import ImageTk, Image

from core.plasma import PlasmaModule
from interfaces.iapp import IApp

class MainWindow(IApp):
    def __init__(self, window:tkinter.Tk, plasma:PlasmaModule):
        """
        :param window: tkinter.TK
        """

        self.set_style()
        self.set_window(window)
        self.set_plasma(plasma)

    def set_plasma(self, plasma:PlasmaModule):
        self.plasma = plasma

    def set_style(self):
        """
        define simulator style

        self.COLOR_BG: simulator background color(hex code)
        self.COLOR_FG: simulator foreground color(hex code)
        self.HEIGHT: simulator window height
        self.WIDTH: simulator window width
        self.START_R: simulator pop initial location(row)
        self.START_C: simulator pop initial location(column)
        self.PARAMETER_Y: input labels location(row)
        self.STOP: stop button flag(if True, freeze)
        self.DONE: show result flag(if True, show result on Output Canvas)
        """
        # === Style ===
        self.COLOR_BG = "#565656"
        self.COLOR_FG = "#d3d3d3"
        # fontStyle = tkFont.Font(family="Courier", size=40)
        self.HEIGHT = 500
        self.WIDTH = 1000
        self.START_R = 100
        self.START_C = 200
        self.PARAMETER_Y_1st = 30
        self.PARAMETER_Y_2nd = 100
        self.STOP = False
        self.DONE = False

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

        self.WINDOW = window

        # == Frame
        self.WINDOW.title("Simulator")
        self.WINDOW.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.START_R}+{self.START_C}")  # CxR+시작c+시작r
        self.WINDOW.resizable(False, False)
        self.WINDOW.config(bg=self.COLOR_BG)

        # == Inputs
        Label(window, text="RPM", font=("Courier", 20, "normal"), bg=self.COLOR_BG, fg=self.COLOR_FG).place(x=100,
                                                                                                            y=self.PARAMETER_Y_1st,
                                                                                                            anchor='n')
        self.rpm_input = Entry(window, width=10)
        self.rpm_input.place(x=200, y=self.PARAMETER_Y_1st, anchor='n')

        Label(window, text="CONVEYOR", font=("Courier", 20, "normal"), bg=self.COLOR_BG, fg=self.COLOR_FG).place(x=350,
                                                                                                                 y=self.PARAMETER_Y_1st,
                                                                                                                 anchor='n')
        self.conveyor_input = Entry(window, width=10)
        self.conveyor_input.place(x=500, y=self.PARAMETER_Y_1st, anchor='n')

        # == Buttons
        self.btnResult = Button(window, text="Result", command=self.run_result, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnResult.place(x=700, y=self.PARAMETER_Y_1st, anchor='n')

        self.btnStop = Button(window, text="Stop", command=self.run_stop, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnStop.place(x=800, y=self.PARAMETER_Y_1st, anchor='n')

        self.btnClear = Button(window, text="Clear", command=self.run_clear, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnClear.place(x=900, y=self.PARAMETER_Y_1st, anchor='n')

        # == Outputs
        self.canvas = Canvas(window, width=900, height=350, relief="solid", bd=2)
        # canvas.create_image(455, 5, image=image, anchor='n')
        self.canvas.place(x=500, y=self.PARAMETER_Y_2nd, anchor='n')

        self.result_images = []
        self.image_on_canvas = self.canvas.create_image(455, 5, image=None, anchor='n')
        self.image = None


    def warn_save_path(self):
        msgbox.showwarning("Warning", "저장 위치를 지정해주세요!")

    def warn_digit(self):
        msgbox.showwarning("Warning", "숫자를 입력해주세요!")

    def run_simulation(self, rpm, conveyor, path):
        self.set_plasma(PlasmaModule(fabric=2000, nPlasma=10, R=130, r=1.5, zoom=10, save_path=path))
        self.plasma.simulation(rpm=rpm, conveyor_speed_m=conveyor, duration_m=10, save=True, imshow=False)

        self.DONE = True

    def run_result(self):
        """
        run simulator
        """

        # == Inputs
        rpm = self.rpm_input.get()
        print(rpm)
        self.rpm_input.delete(0, END)

        conveyor = self.conveyor_input.get()
        print(conveyor)
        self.conveyor_input.delete(0, END)

        # 추후 입력 받도록 수정 필요.
        base_path = '/Users/sujinlee/PycharmProjects/plasma'

        # = check
        if rpm.isdigit() == False or conveyor.isdigit() == False:
            self.warn_digit()
            return

        save_path = f'{base_path}/{rpm}_{conveyor}'

        if os.path.exists(save_path) == False:
            os.mkdir(save_path)
            self.run_simulation(int(rpm), int(conveyor), save_path)
        else:
            self.DONE = True

        if self.DONE == True:
            self.show_result(save_path)

    def run_stop(self):
        print('STOP')
        self.STOP = not self.STOP

    def run_clear(self):
        print('CLEAR')
        self.image = None
        self.STOP = False
        self.DONE = False

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
            if self.STOP == True:
                self.result_images = []
                break

            img_new = Image.open(self.result_images[0])
            print(self.result_images[0])
            self.result_images.pop(0)
            self.image = ImageTk.PhotoImage(img_new.resize((900, 350)))
            self.canvas.itemconfig(self.image_on_canvas, image=self.image)
            self.WINDOW.update()
            # time.sleep(0.005)


if __name__ == "__main__":
    window = Tk()
    MainWindow(window, PlasmaModule)
    window.mainloop()