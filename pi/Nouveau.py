from OLED import OLED
from OLEDWindow import OLEDWindow

# The OLED hardware driver
oled = OLED()

# Two windows on the screen. One is the entire screen. The
# other is a small square over to the right
window_one = OLEDWindow(oled,0,0,256,64)
#window_two = OLEDWindow(oled,130,30,80,30)

for i in range(1,4):
    window_one.DrawHLine(10,i*12,80,0xff)
    window_one.DrawVLine(i*20,5,40,0xff)

window_one.DrawCircle(16,55,3,0xff)
window_one.DrawCircle(29,55,5,0xff)
window_one.DrawCircle(46,55,8,0xff)

window_one.DrawDisc(61,55,3,0xff)
window_one.DrawDisc(73,55,5,0xff)
window_one.DrawDisc(91,55,8,0xff)

window_one.DrawFrame(105,10,40,25,0xff)
window_one.DrawBox(105,40,40,20,0xff)

window_one.DrawRBox(155,10,40,50,7,0xff)
window_one.DrawRFrame(205,10,40,50,7,0xff)

window_one.draw_screen_buffer()

##Two windows on the screen. One is the entire screen. The
##other is a small square over to the right
##
##window_one = OLEDWindow(oled,0,0,256,64)
##window_two = OLEDWindow(oled,256-64,20,32,32)
##for x in xrange(18):
##    window_one.draw_line((0,0),(x*5,63),0x0F)    
##window_one.draw_rectangle(100,10,75,30, 0x0F)
##window_one.draw_rectangle(150,30,50,30, 0x0F)
###
##window_one.draw_screen_buffer()
##
### Draw second window on top of first
##
##window_two.draw_rectangle(0,0,31,31,0x04)
###raw_input("ENTER")
##for x in xrange(16):
##    window_two.draw_rectangle(x+2,x+2,12,12,0x04)
##    
##window_two.draw_screen_buffer()
