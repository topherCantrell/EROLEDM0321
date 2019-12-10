import math
import tkinter

from oled.oled_window import OLEDWindow


class OLED(tkinter.Canvas):

    COLORS = ['#000', '#001', '#002', '#003', '#004', '#005', '#006', '#007', '#008', '#009', '#00A', '#00B', '#00C', '#00D', '#00E', '#00F']

    def __init__(self, parent):
        super().__init__(parent)
        self._pixels = [0] * 256 * 64
        self._data_pass = 0

    def set_data_window(self, x, y, width, height):
        pass

    def Write_Instruction(self, cmd):
        pass

    def writeDataBytes(self, data):
        if self._data_pass == 0:
            self._data_pass = 1
            ptr = 0
        else:
            ptr = 256 * 32

        for d in data:
            a = d >> 4
            b = d & 0xF
            self._pixels[ptr] = a
            self._pixels[ptr + 1] = b
            ptr = ptr + 2

        if self._data_pass == 1:
            self.draw()

    def draw(self):
        for y in range(64):
            for x in range(256):
                color = OLED.COLORS[self._pixels[y * 256 + x]]
                self.create_rectangle(x * 4, y * 4, x * 4 + 4, y * 4 + 4, fill=color, width=0)


BOX_SIZE = 8
BOX_SPACE = 6

top = tkinter.Tk()
top.geometry('1024x256+300+300')

oled = OLED(top)

window = OLEDWindow(oled, 0, 0, 256, 64)

x = 4
y = 4

hours = 23
minutes = 47

hours_a = bin(int(hours / 10))[2:]
while(len(hours_a)) < 4:
    hours_a = '0' + hours_a
hours_b = bin(int(hours % 10))[2:]
while(len(hours_b)) < 4:
    hours_b = '0' + hours_b
mins_a = bin(int(minutes / 10))[2:]
while(len(mins_a)) < 4:
    mins_a = '0' + mins_a
mins_b = bin(int(minutes % 10))[2:]
while(len(mins_b)) < 4:
    mins_b = '0' + mins_b

col_values = [hours_a, hours_b, mins_a, mins_b]

for cols in range(4):
    for rows in range(4):
        if cols == 0 and rows == 0:
            continue
        if cols == 0 and rows == 1:
            continue
        if cols == 2 and rows == 0:
            continue
        if cols > 1:
            ofs = BOX_SPACE * 2
        else:
            ofs = 0

        if col_values[cols][rows] == '1':
            window.DrawBox(x + cols * (BOX_SIZE + BOX_SPACE) + ofs, y + rows * (BOX_SIZE + BOX_SPACE), BOX_SIZE, BOX_SIZE, 15)
        else:
            window.draw_rectangle(x + cols * (BOX_SIZE + BOX_SPACE) + ofs, y + rows * (BOX_SIZE + BOX_SPACE), BOX_SIZE, BOX_SIZE, 15)


window.draw_screen_buffer()

oled.pack(fill=tkinter.BOTH, expand=1)

top.mainloop()
