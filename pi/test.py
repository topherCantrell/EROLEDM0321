from OLED import OLED

oled = OLED()

for x in xrange(18):
    oled.draw_line((0,0),(x*5,63),0xFF)
    
oled.draw_rectangle(100,10,75,30, 0xFF)
oled.draw_rectangle(150,30,50,30, 0xFF)
        
oled.draw_screen_buffer()


