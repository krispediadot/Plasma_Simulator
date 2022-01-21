import os
import time
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox as msgbox

from PIL import ImageTk, Image

class MainWindow():
    def __init__(self, window):
        self.window = window

        # === Style
        self.COLOR_BG = "#565656"
        self.COLOR_FG = "#d3d3d3"
        # fontStyle = tkFont.Font(family="Courier", size=40)
        self.HEIGHT = 500
        self.WIDTH = 1000
        self.START_R = 100
        self.START_C = 200

        self.PARAMETER_Y = 30

        self.STOP = False

        self.window.title("Simulator")
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.START_R}+{self.START_C}")  # CxR+시작c+시작r
        self.window.resizable(False, False)
        self.window.config(bg=self.COLOR_BG)

        Label(window, text="RPM", font=("Courier", 20, "normal"), bg=self.COLOR_BG, fg=self.COLOR_FG).place(x=100, y=self.PARAMETER_Y, anchor='n')
        self.rpm_input = Entry(window, width=10)
        self.rpm_input.place(x=200, y=self.PARAMETER_Y, anchor='n')

        Label(window, text="CONVEYOR", font=("Courier", 20, "normal"), bg=self.COLOR_BG, fg=self.COLOR_FG).place(x=350, y=self.PARAMETER_Y, anchor='n')
        self.conveyor_input = Entry(window, width=10)
        self.conveyor_input.place(x=500, y=self.PARAMETER_Y, anchor='n')

        self.canvas = Canvas(window, width=900, height=350, relief="solid", bd=2)
        # canvas.create_image(455, 5, image=image, anchor='n')
        self.canvas.place(x=500, y=100, anchor='n')

        self.btnResult = Button(window, text="Result", command=self.run, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnResult.place(x=700, y=self.PARAMETER_Y, anchor='n')

        self.btnStop = Button(window, text="Stop", command=self.stop, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnStop.place(x=800, y=self.PARAMETER_Y, anchor='n')

        self.btnClear = Button(window, text="Clear", command=self.clear, bg=self.COLOR_FG, fg=self.COLOR_BG)
        self.btnClear.place(x=900, y=self.PARAMETER_Y, anchor='n')

        self.result_images = []
        self.image_on_canvas = self.canvas.create_image(455, 5, image=None, anchor='n')
        self.image = None

    def warn_digit(self):
        msgbox.showwarning("Warning", "숫자를 입력해주세요!!")

    def run(self):

        # 1. 입력 받음
        rpm = self.rpm_input.get()
        print(rpm)
        self.rpm_input.delete(0, END)

        conveyor = self.conveyor_input.get()
        print(conveyor)
        self.conveyor_input.delete(0, END)

        # 1.1 숫자 아니면 다시 입력
        if rpm.isdigit() == False or conveyor.isdigit() == False:
            self.warn_digit()
            return

        self.SAVE_PATH = '/Users/sujinlee/PycharmProjects/plasma/120_10000_1024_512'
        self.show_result(self.SAVE_PATH)

    def stop(self):
        print('STOP')
        self.STOP = not self.STOP

    def clear(self):
        print('CLEAR')
        self.image = None
        self.STOP = False

    def show_result(self, SAVE_PATH):
        for file in os.listdir(SAVE_PATH):
            self.result_images.append(os.path.join(SAVE_PATH, file))
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
            self.window.update()
            # time.sleep(0.005)


if __name__ == "__main__":
    window = Tk()
    MainWindow(window)
    window.mainloop()