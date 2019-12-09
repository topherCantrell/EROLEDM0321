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


SEVEN_SEGS = [
    'abcdef',  # 0
    'bc',  # 1
    'abdeg',  # 2
    'abcdg',  # 3
    'bcfg',  # 4
    'acdfg',  # 5
    'acdefg',  # 6
    'abc',  # 7
    'abcdefg',  # 8
    'abcdfg',  # 9
]

DIGIT_ANGLES = [
    math.pi / 12 * 11,  # 4
    math.pi / 12 * 10,  # 5
    math.pi / 12 * 9,   # 6
    math.pi / 12 * 8,   # 7
    math.pi / 12 * 7,   # 8
    math.pi / 12 * 6,   # 9
    math.pi / 12 * 5,   # 10
    math.pi / 12 * 4,   # 11
    math.pi / 12 * 3,   # 12
    math.pi / 12 * 2,   # 1
    math.pi / 12 * 1,   # 2
    math.pi / 12 * 0,   # 3
]


def sevenSegDigit(window, x, y, size, num, color):
    spec = SEVEN_SEGS[num]
    if 'a' in spec:
        window.draw_line((x, y), (x + size, y), color)
    if 'b' in spec:
        window.draw_line((x + size, y), (x + size, y + size), color)
    if 'c' in spec:
        window.draw_line((x + size, y + size), (x + size, y + size * 2), color)
    if 'd' in spec:
        window.draw_line((x, y + size * 2), (x + size, y + size * 2), color)
    if 'e' in spec:
        window.draw_line((x, y + size), (x, y + size * 2), color)
    if 'f' in spec:
        window.draw_line((x, y), (x, y + size), color)
    if 'g' in spec:
        window.draw_line((x, y + size), (x + size, y + size), color)


top = tkinter.Tk()
top.geometry('1024x256+300+300')

oled = OLED(top)

window = OLEDWindow(oled, 0, 0, 256, 64)


window.DrawCircle(128, 32, 30, 15)
window.DrawCircle(128, 32, 29, 15)
window.DrawBox(125, 29, 4, 4, 15)

# Radius 32

SIZE = 3

for i in range(12):
    angle = (math.pi * 2 / 12) * i - math.pi / 2
    x1 = 128 + int(math.cos(angle) * 20)
    y1 = 32 + int(math.sin(angle) * 20)
    x2 = 128 + int(math.cos(angle) * 26)
    y2 = 32 + int(math.sin(angle) * 26)
    x3 = 128 + int(math.cos(angle) * 30)
    y3 = 32 + int(math.sin(angle) * 30)
    window.draw_line((x2, y2), (x3, y3), 15)
    sevenSegDigit(window, x1 - int(SIZE / 2), y1 - SIZE, SIZE, i % 10, 8)

hour = (math.pi * 2 / 12) * 3.5 - math.pi / 2
min = (math.pi * 2 / 12) * 10 - math.pi / 2

window.draw_line((128, 32), (128 + int(math.cos(hour) * 15), 32 + int(math.sin(hour) * 15)), 15)
window.draw_line((128, 32), (128 + int(math.cos(min) * 25), 32 + int(math.sin(min) * 25)), 15)


window.draw_screen_buffer()

oled.pack(fill=tkinter.BOTH, expand=1)

top.mainloop()
