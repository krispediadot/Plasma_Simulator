import os
import time
import tkinter
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox as msgbox

from PIL import ImageTk, Image

class MainWindow():
    def __init__(self, window:tkinter.Tk, savePath:str):
        """
        :param window: tkinter.TK
        :param savePath: string
        """
        self.WINDOW = window
        self.SAVE_PATH = savePath

        self.setStyle()
        self.setWindow()

    def setStyle(self):
        """
        define simulator style

        COLOR_BG: simulator background color(hex code)
        COLOR_FG: simulator foreground color(hex code)
        HEIGHT: simulator window height
        WIDTH: simulator window width
        START_R: simulator pop initial location(row)
        START_C: simulator pop initial location(column)
        PARAMETER_Y: input labels location(row)
        STOP: stop button flag(if True, freeze)
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
        self.STOP = False

    def setWindow(self):
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
        self.btnResult = Button(window, text="Result", command=self.runResult, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnResult.place(x=700, y=self.PARAMETER_Y_1st, anchor='n')

        self.btnStop = Button(window, text="Stop", command=self.runStop, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnStop.place(x=800, y=self.PARAMETER_Y_1st, anchor='n')

        self.btnClear = Button(window, text="Clear", command=self.runClear, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnClear.place(x=900, y=self.PARAMETER_Y_1st, anchor='n')

        # == Outputs
        self.canvas = Canvas(window, width=900, height=350, relief="solid", bd=2)
        # canvas.create_image(455, 5, image=image, anchor='n')
        self.canvas.place(x=500, y=100, anchor='n')

        self.result_images = []
        self.image_on_canvas = self.canvas.create_image(455, 5, image=None, anchor='n')
        self.image = None


    def warnSavePath(self):
        msgbox.showwarning("Warning", "저장 위치를 지정해주세요!")

    def warnDigit(self):
        msgbox.showwarning("Warning", "숫자를 입력해주세요!")

    def runResult(self):
        """
        run simulator
        """
        # 1. 입력 받음
        rpm = self.rpm_input.get()
        print(rpm)
        self.rpm_input.delete(0, END)

        conveyor = self.conveyor_input.get()
        print(conveyor)
        self.conveyor_input.delete(0, END)

        # 1.1 숫자 아니면 다시 입력
        if rpm.isdigit() == False or conveyor.isdigit() == False:
            self.warnDigit()
            return

        self.showResult()

    def runStop(self):
        print('STOP')
        self.STOP = not self.STOP

    def runClear(self):
        print('CLEAR')
        self.image = None
        self.STOP = False

    def showResult(self):
        """
        open result images & display the images on simulator
        """
        for file in os.listdir(self.SAVE_PATH):
            self.result_images.append(os.path.join(self.SAVE_PATH, file))
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
    savePath = '/Users/sujinlee/PycharmProjects/plasma/120_10000_1024_512'

    window = Tk()
    MainWindow(window, savePath)
    window.mainloop()