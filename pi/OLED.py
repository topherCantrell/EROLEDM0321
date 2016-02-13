import spidev
import time
import RPi.GPIO as GPIO

class OLED:
    
    # Display is 256x64 pixels, 2 pixels per byte. The most-significant nibble
    # is the left pixel.
    
    # Screen buffer is thus 256 * 64 / 2 = 8192 (8K)
    
    # Write your pixels to the screen buffer and then "draw_screen_buffer"
    
    # Graphics functions that draw in the buffer:
    #   set_pixel(x,y,color)
    #   draw_line( (x1,y1), (x2,y2), color)
    #   draw_rectangle( x,y,width,height, color)
    
    # It takes over one second to draw the entire screen buffer.    
    # TODO: Update this driver to allow for "windows" on the display that
    # can be refreshed independently.
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(25,GPIO.OUT)   # 25 RESET (low to reset)
        GPIO.output(25,True)      #    Release the RESET
        GPIO.setup(24,GPIO.OUT)   # 24 D/C
        self.spi = spidev.SpiDev()     # Init the spidev module
        self.spi.open(0,0)             # Open the spi device
        self.spi.cshigh = False        # CS active low
        self.spi.lsbfirst = False      # Send MSB first
        self.spi.mode = 3              # Clock idle high, data on 2nd edge (end of pulse)
        self.spi.max_speed_hz = 5000000
        
        self.resetOLED()  
                
        self.Write_Instruction(0xFD) # Set Command Lock
        
        self.Write_Instruction(0xFD) # SET COMMAND LOCK 
        self.Write_Data(0x12) # UNLOCK 
        self.Write_Instruction(0xAE) # DISPLAY OFF 
        self.Write_Instruction(0xB3) # DISPLAYDIVIDE CLOCKRADIO/OSCILLATAR FREQUANCY*/ 
        self.Write_Data(0x91) 
        self.Write_Instruction(0xCA) # multiplex ratio 
        self.Write_Data(0x3F) # duty = 1/64 
        self.Write_Instruction(0xA2) # set offset 
        self.Write_Data(0x00)
        self.Write_Instruction(0xA1) # start line 
        self.Write_Data(0x00)
        self.Write_Instruction(0xA0) #set remap
        self.Write_Data(0x14)
        self.Write_Data(0x11)
        
        self.Write_Instruction(0xAB) # funtion selection 
        self.Write_Data(0x01) # selection external vdd  
        self.Write_Instruction(0xB4)
        self.Write_Data(0xA0)
        self.Write_Data(0xfd) 
        self.Write_Instruction(0xC1) # set contrast current  
        self.Write_Data(0x80)
        self.Write_Instruction(0xC7) # master contrast current control 
        self.Write_Data(0x0f)
         
        self.Write_Instruction(0xB1) # SET PHASE LENGTH
        self.Write_Data(0xE2)
        self.Write_Instruction(0xD1)
        self.Write_Data(0x82)
        self.Write_Data(0x20) 
        self.Write_Instruction(0xBB) # SET PRE-CHANGE VOLTAGE 
        self.Write_Data(0x1F)
        self.Write_Instruction(0xB6) # SET SECOND PRE-CHARGE PERIOD
        self.Write_Data(0x08)
        self.Write_Instruction(0xBE) # SET VCOMH  
        self.Write_Data(0x07)
        self.Write_Instruction(0xA6) # normal display 
        self.Clear_ram()
        self.Write_Instruction(0xAF) # display ON
        
        # Make and clear the screen buffer
        self.screenBuffer = [0]*8192

    def resetOLED(self):
        GPIO.output(25,False) # Activate reset
        time.sleep(0.5 )      # Hold it low for half a second
        GPIO.output(25,True)  # Release reset
        time.sleep(1.0)       # Give the chip a second to come up
    
    def Write_Instruction(self,dataByte):
        GPIO.output(24,False) # Select command register
        self.spi.writebytes([dataByte])
        
    def Write_Data(self,dataByte):
        GPIO.output(24,True) # Select data register
        self.spi.writebytes([dataByte])    
    
    def writeDataBytes(self,dataBytes):
        GPIO.output(24,True) # Select data register
        self.spi.writebytes(dataBytes)
        
    def Clear_ram(self):
        self.Write_Instruction(0x15) 
        self.Write_Data(0x00)
        self.Write_Data(0x77) 
        self.Write_Instruction(0x75) 
        self.Write_Data(0x00)
        self.Write_Data(0x7f) 
        self.Write_Instruction(0x5C)    
        for y in xrange(128):
            for x in xrange(120):
                self.Write_Data(0x00)   
    
    def Set_Row_Address(self,add):
        self.Write_Instruction(0x75) # SET SECOND PRE-CHARGE PERIOD 
        add = 0x3f & add
        self.Write_Data(add)
        self.Write_Data(0x3f)
    
    def Set_Column_Address(self,add):
        add = 0x3f & add
        self.Write_Instruction(0x15) # SET SECOND PRE-CHARGE PERIOD  
        self.Write_Data(0x1c+add)
        self.Write_Data(0x5b)
    
    def draw_screen_buffer(self):
        self.Set_Row_Address(0)
        self.Set_Column_Address(0)
        self.Write_Instruction(0x5c)
        
        for m in xrange(8192):
            self.Write_Data(self.screenBuffer[m])
        
    def set_pixel(self,x,y,color):
        color = color & 0x0F
        ofs = y * 128 # 128 bytes (256 pixels) per row
        ofs = ofs + x/2 # 2 pixels per byte across row
        if x%2 ==0: # even
            v = self.screenBuffer[ofs] & 0x0F
            v = v | (color<<4)
        else:
            v = self.screenBuffer[ofs] & 0xF0
            v = v | color
        self.screenBuffer[ofs] = v     
        
    def draw_line(self,start, end,color):
        """Bresenham's Line Algorithm       
        """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
     
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
     
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
     
        # Swap start and end points if necessary and store swap state
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
     
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
     
        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1
     
        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            #
            self.set_pixel(coord[0],coord[1],color)
            #
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx       
    
    def draw_rectangle(self,x,y,width,height, color):
        for xx in xrange(width):
            self.set_pixel(x+xx,y,color)
            self.set_pixel(x+xx,y+height-1, color)
        for yy in xrange(height):
            self.set_pixel(x,y+yy,color)
            self.set_pixel(x+width-1,y+yy,color)