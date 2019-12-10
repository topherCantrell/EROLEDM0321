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
                self.create_rectangle(x * 4 + 2, y * 4 + 2, x * 4 + 4 + 2, y * 4 + 4 + 2, fill=color, width=0)


top = tkinter.Tk()
top.geometry('1025x257+300+300')

oled = OLED(top)

window = OLEDWindow(oled, 0, 0, 256, 64)

window.draw_text(2, 0, 'IT IS  HALF TEN', 15)
window.draw_text(2, 8, 'QUARTER  TWENTY', 15)
window.draw_text(2, 16, 'FIVE MINUTES TO', 15)
window.draw_text(2, 24, 'PAST TWO  THREE', 15)
window.draw_text(2, 32, 'ONE  FOUR  FIVE', 15)
window.draw_text(2, 40, 'SIX SEVEN EIGHT', 15)
window.draw_text(2, 48, 'NINE TEN ELEVEN', 15)
window.draw_text(2, 56, "TWELVE  O'CLOCK", 15)


window.draw_screen_buffer()

oled.pack(fill=tkinter.BOTH, expand=1)

top.mainloop()
