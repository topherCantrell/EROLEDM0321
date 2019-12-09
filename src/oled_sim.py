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


top = tkinter.Tk()
top.geometry('1024x256+300+300')

oled = OLED(top)

window = OLEDWindow(oled, 0, 0, 256, 64)

"""
for i in range(1, 4):
    window.DrawHLine(10, i * 11, 83, 0xf)
    window.DrawVLine(i * 20, 2, 40, 0xf)

window.DrawCircle(10, 55, 3, 0xf)
window.DrawCircle(23, 55, 5, 0xf)
window.DrawCircle(40, 55, 8, 0xf)

window.DrawDisc(56, 55, 3, 0xf)
window.DrawDisc(67, 55, 5, 0xf)
window.DrawDisc(85, 55, 8, 0xf)

window.DrawFrame(100, 5, 25, 25, 0xf)
window.DrawBox(100, 35, 25, 25, 0xf)

window.DrawRBox(130, 5, 40, 55, 7, 0xf)
window.DrawRFrame(175, 5, 40, 55, 7, 0xf)

window.DrawTriangle(217, 60, 255, 60, 236, 5, 0xf)
"""

window.DrawCircle(128, 32, 30, 15)
window.DrawCircle(128, 32, 29, 15)


window.draw_text(148, 29, '3', 15, 5)
window.draw_text(104, 29, '9', 15, 5)
window.draw_text(126, 50, '6', 15, 5)


#window.draw_text(105, 21, '10', 15, 5)
#window.draw_text(114, 12, '11', 15, 5)
window.draw_text(123, 8, '12', 15, 5)

'''
(158, 32)
(153, 46)
(143, 57)
(128, 62)
(114, 57)
(103, 47)
(98, 32)
(103, 18)
(113, 7) 11
(128, 2) 12
(142, 7) 1
(153, 17) 2
'''

# Radius 32

for i in range(12):
    angle = (math.pi * 2 / 12) * i
    x1 = 128 + int(math.cos(angle) * 30)
    y1 = 32 + int(math.sin(angle) * 30)
    x2 = 128 + int(math.cos(angle) * 26)
    y2 = 32 + int(math.sin(angle) * 26)
    window.draw_line((x1, y1), (x2, y2), 15)

window.draw_screen_buffer()

oled.pack(fill=tkinter.BOTH, expand=1)

top.mainloop()
