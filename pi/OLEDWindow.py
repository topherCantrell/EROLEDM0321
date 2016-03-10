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


#########################################################################


    def DrawVLine(self,x,y,h,color):                # Draw vertical line
        self.draw_line((x, y), (x, y+h-1), color)
        
    def DrawHLine(self, x, y, w, color):            # Draw horizontal line
        self.draw_line((x, y), (x+w-1, y), color)
        
    def DrawFrame(self, x, y, w, h, color):         # Draw_rectangle alternative
        self.DrawHLine(x, y, w, color)
        self.DrawHLine(x, y+h-1, w, color)
        self.DrawVLine(x, y, h, color)
        self.DrawVLine(x+w-1, y, h, color)

    def DrawRFrame(self, x, y, w, h, r, color):     # Draw Rounded Corners Rectangle 
        self.DrawHLine(x+r, y, w-2*r, color)      # Top
        self.DrawHLine(x+r, y+h-1, w-2*r, color)  # Bottom
        self.DrawVLine(x, y+r, h-2*r, color)      # Left
        self.DrawVLine(x+w-1, y+r, h-2*r, color)  # Right
        # draw four corners
        self.DrawCircleHelper(x+r, y+r, r, 1, color)
        self.DrawCircleHelper(x+w-r-1, y+r, r, 2, color)
        self.DrawCircleHelper(x+w-r-1, y+h-r-1, r, 4, color)
        self.DrawCircleHelper(x+r, y+h-r-1, r, 8, color)
        
    def DrawBox(self, x, y, w, h, color):           # Draw Filled Rectangle
        for t in range(x, x+w):
            self.DrawVLine(t, y, h, color)
            
    def DrawRBox(self, x, y, w, h, r, color):       # Draw Rounded Corners Filled Rectangle
        self.DrawBox(x+r, y, w-2*r, h, color)
        # draw four corners
        self.FillCircleHelper(x+w-r-1, y+r, r, 1, h-2*r-1, color)
        self.FillCircleHelper(x+r    , y+r, r, 2, h-2*r-1, color)
            
    def DrawCircle(self, x0, y0, r, color):         # Draw Circle
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        self.set_pixel(x0, y0+r, color)
        self.set_pixel(x0, y0-r, color)
        self.set_pixel(x0+r, y0, color)
        self.set_pixel(x0-r, y0, color)

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
                
            x += 1
            ddF_x += 2
            f += ddF_x
  
            self.set_pixel(x0+x, y0+y, color)
            self.set_pixel(x0-x, y0+y, color)
            self.set_pixel(x0+x, y0-y, color)
            self.set_pixel(x0-x, y0-y, color)
            self.set_pixel(x0+y, y0+x, color)
            self.set_pixel(x0-y, y0+x, color)
            self.set_pixel(x0+y, y0-x, color)
            self.set_pixel(x0-y, y0-x, color)
            
    def DrawDisc(self, x0, y0, r, color):
        self.DrawVLine(x0, y0-r, 2*r+1, color)
        self.FillCircleHelper(x0, y0, r, 3, 0, color)


    def DrawCircleHelper(self, x0, y0, r, cornername, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
    
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
                
            x += 1
            ddF_x += 2
            f += ddF_x
            
            if (cornername & 0x4):
                self.set_pixel(x0 + x, y0 + y, color)
                self.set_pixel(x0 + y, y0 + x, color)
                 
            if (cornername & 0x2):
                self.set_pixel(x0 + x, y0 - y, color)
                self.set_pixel(x0 + y, y0 - x, color)
                
            if (cornername & 0x8):
                self.set_pixel(x0 - y, y0 + x, color)
                self.set_pixel(x0 - x, y0 + y, color)
                
            if (cornername & 0x1):
                self.set_pixel(x0 - y, y0 - x, color)
                self.set_pixel(x0 - x, y0 - y, color)
                
    def FillCircleHelper(self, x0, y0, r, cornername, delta, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        
        while x < y:
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y

            x += 1
            ddF_x += 2
            f += ddF_x

            if (cornername & 0x1):
                self.DrawVLine(x0+x, y0-y, 2*y+1+delta, color)
                self.DrawVLine(x0+y, y0-x, 2*x+1+delta, color)

            if (cornername & 0x2):
                self.DrawVLine(x0-x, y0-y, 2*y+1+delta, color)
                self.DrawVLine(x0-y, y0-x, 2*x+1+delta, color)
