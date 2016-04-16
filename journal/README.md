# Journal

## 4/16/2016

Scoobie and Davey making some great contributions.

## 2/13/2016

I had moved the jumpers on the back of the display to "8080 Parallel" for a propeller project. Once I put them back on "4 wire SPI" it works great.

I got the OLED.py class working. It implements an 8K screen buffer and a few X,Y,COLOR based drawing functions. Once the buffer is setup you call "draw_screen_buffer" to refresh the entire RAM. This takes over one second. The serial
solution is terribly slow. I am hoping the parallel/Propeller version will be fast.

Turns out you can tell the OLED about the window (x,y,width,height) you are filling data into and it will advance the data cursor through RAM appropriately. That made the window implementation trivial.

DONE: Add a general text library with text pictures
TODO: make a Propeller (parallel) version

## 2/12/2016

Frustrating. I tried to hook the display up again but I don't get anything. I'm using the Pi2 this time. I guess I can try the old Pi. And maybe break out the scope. Sigh. I wanted this part to just work.