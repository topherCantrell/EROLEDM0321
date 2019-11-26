from OLED import OLED
from OLEDWindow import OLEDWindow

# The OLED hardware driver
oled = OLED()

# Two windows on the screen. One is the entire screen. The
# other is a small square over to the right
window_one = OLEDWindow(oled,0,0,256,64)
window_two = OLEDWindow(oled,256-64,20,32,32)

for x in range(18):
    window_one.draw_line((0,0),(x*5,63),0x0F)    
window_one.draw_rectangle(100,10,75,30, 0x0F)
window_one.draw_rectangle(150,30,50,30, 0x0F)
#
window_one.draw_screen_buffer()

# Draw second window on top of first

window_two.draw_rectangle(0,0,31,31,0x04)
for x in range(16):
    window_two.draw_rectangle(x+2,x+2,10,10,0x04)
#    
window_two.draw_screen_buffer()

