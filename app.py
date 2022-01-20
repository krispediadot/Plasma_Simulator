import os
import time
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox as msgbox


# === Style
COLOR_BG = "#565656"
COLOR_FG = "#d3d3d3"
# fontStyle = tkFont.Font(family="Courier", size=40)
HEIGHT = 500
WIDTH = 1000
START_R = 100
START_C = 200

PARAMETER_Y = 30

# ===
def warn_digit():
    msgbox.showwarning("Warning", "숫자를 입력해주세요!!")

def run():
    found = False
    # 1. 입력 받음
    rpm = rpm_input.get()
    print(rpm)
    rpm_input.delete(0, END)

    conveyor = conveyor_input.get()
    print(conveyor)
    conveyor_input.delete(0, END)

    # 1.1 숫자 아니면 다시 입력
    if rpm.isdigit() == False or conveyor.isdigit() == False:
        warn_digit()
        return

# ===
window = Tk()

window.title("Simulator")
window.geometry(f"{WIDTH}x{HEIGHT}+{START_R}+{START_C}") # CxR+시작c+시작r
window.resizable(False, False)
window.config(bg=COLOR_BG)

Label(window, text="RPM", font=("Courier", 20, "normal"), bg=COLOR_BG, fg=COLOR_FG).place(x=150, y=PARAMETER_Y, anchor='n')
rpm_input = Entry(window, width=10)
rpm_input.place(x=250, y=PARAMETER_Y, anchor='n')

Label(window, text="CONVEYOR", font=("Courier", 20, "normal"), bg=COLOR_BG, fg=COLOR_FG).place(x=450, y=PARAMETER_Y, anchor='n')
conveyor_input = Entry(window, width=10)
conveyor_input.place(x=600, y=PARAMETER_Y, anchor='n')

btnFind = Button(window, text="Result", command=run, bg=COLOR_FG, fg=COLOR_BG)
btnFind.place(x=800, y=PARAMETER_Y, anchor='n')

# print(os.getcwd())
# IMAGE = '/Users/sujinlee/PycharmProjects/plasma/a.png'
# image = PhotoImage(file=IMAGE)

canvas = Canvas(window, width=900, height=350, relief="solid", bd=2)
canvas.place(x=500, y=100, anchor='n')

window.mainloop()