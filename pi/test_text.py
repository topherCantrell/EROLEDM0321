from OLED import OLED
from OLEDWindow import OLEDWindow

# The OLED hardware driver
oled = OLED()

window_one = OLEDWindow(oled,0,0,256,64)

for y in range(4):
    mes = ""
    for x in range(32):
        mes = mes + chr(y*32+x) 
    window_one.draw_text(0,y*8,mes,8)
    
window_one.draw_big_text(0,48,"Big and dim !",2)

window_one.draw_screen_buffer()

