class OLEDWindow:
    
    # A window area on the OLED screen. The OLED hardware allows
    # you to set the data cursor to respect row/column boundaries.
    # Thus writes automatically scroll inside a smaller window. That
    # makes this class easy to implement.
    #
    # X coordinates and WIDTH values must be multiples of 4 pixels. This
    # is a hardware constraint.
    
    def __init__(self, oled, x, y, width, height):
        # x and width must be multiples of 4
        self.x = x
        self.y = y
        self.width = (width/4)*4
        self.height = height
        self.oled = oled
        # Make and clear the screen buffer
        self.screenBuffer = [0]*(width/2)*height
        
    def draw_screen_buffer(self):
        self.oled.set_data_window(self.x,self.y,self.width,self.height)        
        self.oled.Write_Instruction(0x5c)        
        for m in xrange(len(self.screenBuffer)):
            self.oled.Write_Data(self.screenBuffer[m])
        
    def set_pixel(self,x,y,color):
        color = color & 0x0F
        ofs = y * self.width/2
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
           
    