from OLED import OLED
from OLEDWindow import OLEDWindow

# The OLED hardware driver
oled = OLED()

window_one = OLEDWindow(oled,0,0,256,64)
# window_two = OLEDWindow(oled,130,30,80,30)   # not used

for i in range(1,4):
    window_one.DrawHLine(10,i*11,83,0xf)
    window_one.DrawVLine(i*20,2,40,0xf)

window_one.DrawCircle(10,55,3,0xf)
window_one.DrawCircle(23,55,5,0xf)
window_one.DrawCircle(40,55,8,0xf)

window_one.DrawDisc(56,55,3,0xf)
window_one.DrawDisc(67,55,5,0xf)
window_one.DrawDisc(85,55,8,0xf)

window_one.DrawFrame(100,5,25,25,0xf)
window_one.DrawBox(100,35,25,25,0xf)

window_one.DrawRBox(130,5,40,55,7,0xf)
window_one.DrawRFrame(175,5,40,55,7,0xf)

window_one.DrawTriangle(217, 60, 255, 60, 236, 5, 0xf)

window_one.draw_screen_buffer()

