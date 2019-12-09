import tkinter
from oled.oled_window import OLEDWindow

class OLED(tkinter.Canvas):
    
    COLORS = ['#000','#001','#002','#003','#004','#005','#006','#007','#008','#009','#00A','#00B','#00C','#00D','#00E','#00F']
    
    def __init__(self,parent):
        super().__init__(parent)
        self._pixels = [0]*256*64
        self._data_pass = 0
                
    def set_data_window(self,x,y,width,height):
        pass
    
    def Write_Instruction(self,cmd):
        pass
    
    def writeDataBytes(self,data):
        print(len(data))
    
    def draw(self):         
        for y in range(64):
            for x in range(256):                
                color = OLED.COLORS[self._pixels[y*256+x]]
                self.create_rectangle(x*4,y*4,x*4+4,y*4+4, fill=color,width=0)
  
top = tkinter.Tk()
top.geometry('1024x256+300+300')

oled = OLED(top)

window = OLEDWindow(oled,0,0,256,64)

window.DrawBox(100,35,25,25,0xf)
window.draw_screen_buffer()

oled.draw()
oled.pack(fill=tkinter.BOTH, expand=1)

top.mainloop()

