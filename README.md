ER-OLEDM032-1
=============

The ER-OLEDM032-1 is a 256x64 graphical OLED display. Each pixel is a 4-bit gray-scale value.

[http://www.buydisplay.com/default/oled-3-2-inch-displays-module-companies-with-driver-circuit-blue-on-black](http://www.buydisplay.com/default/oled-3-2-inch-displays-module-companies-with-driver-circuit-blue-on-black)

The display board has four different interface options. I used the 4-wire SPI mode in this project to connect
the display to a Raspberry Pi.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/oled-pi.jpg)

## Hardware 

The display has four different interface modes selected by jumpers on the back of the board. The jumpers are actually
two 0 Ohm surface mount resistors you must move to select the desired interface. See the interface documentation for
details.

[https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/docs/ER-OLEDM032-1_Interfacing.pdf](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/docs/ER-OLEDM032-1_Interfacing.pdf?raw=true)

The interface options are:
- 8-bit parallel for 6800 series microprocessor
- 8-bit parallel for 8080 series microprocessor
- 3-wire SPI interface
- 4-wire SPI interface

My board arrived with the jumpers set for "8-bit parallel for 6800 series microprocessor". I carefully changed the
jumpers to "4-wire SPI interface".

Usually "4-wire SPI" means that both MOSI and MISO wires are used in a bidirectional connection. Usually "3-wire SPI" means that
MOSI and MISO are combined into a single SI/SO line that handles communication.

The SPI interface to the ER-OLEDM032 never sends data back to the processor. Despite the "3-wire" and "4-wire" terminology in the
display documentation the interface is ALWAYS the traditional-4-wire-SPI, but the MISO wire is ignored.

The term "4-wire" in the documentation refers to an extra signaling wire that is unrelated to the SPI interface.

You talk to the display by sending a COMMAND byte followed by several DATA bytes. You must tell the display whether the byte
you are writing is to be interpreted as a COMMAND or DATA. In the "4-wire" interface option you use a separate wire to
select COMMAND or DATA. In the "3-wire" interface option you send the select as the first bit in a NINE bit SPI sequence.

The native SPI library on the Raspberry Pi has trouble sending 9-bit bytes. I used the extra COMMAND/DATA wire and normal
8-bit SPI writes.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/connect.jpg)

## Software 

The display uses a Solomon Systech chip, the SSD1322, to drive the display. The CMOS chip has many control registers and
command sequences described in the reference manual:

[https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/docs/SSD1132.pdf](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/docs/SSD1322.pdf?raw=true)

The chip is designed for a 480x128 OLED display, but its registers can be configured to work with
the 256x64 display.

The company has published demo code for the 256x64 display. The code is written in C. The code includes the initialization
sequence and routines to draw on the display.

[https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/docs/ER-OLEDM032-1_DemoCode.txt](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/docs/ER-OLEDM032-1_DemoCode.txt)

I translated this C code to Python for use on the Raspberry Pi. See pi/RPI_OLED.py in this project.

The demo code initializes the display and draws several screens. Then it enters a loop allowing you to type in
new contrast values (0 to 255).

These photographs of the running display (pardon the poor quality) show several of the screens from the demo.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/DemoRun.jpg)

## Screen Buffer

The OLED.py module contains the OLED class that drives the OLED hardware.

The OLEDWindow.py module contains a window implementation over the OLED object. You pass in the OLED
driver object and the window parameters (x,y,width,height). The OLEDWindow object keeps a screen
buffer for the defined window and draws it on the OLED hardware when prompted.

You fill the windows with your graphics and draw the windows in the order you want them drawn on top of
each other. There is no transparency between windows.

You fill the window with your graphics using methods like "set_pixel", "draw_line", and 
"draw_rectangle". Then call "draw_screen_buffer" to copy the buffer to the display.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/raster.png)

Scoobie Snax in Italy added a lot of features to the code. Here is his test_shapes code.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/testShapes.jpg)

I added text printing to the code.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/text.JPG)


