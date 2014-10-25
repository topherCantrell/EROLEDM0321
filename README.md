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

Link to interface document. 4-wire.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/connect.jpg)

## Software 

Have to setup several registers. Link to SSD.

Link to Demo Code. Translated to python on the raspberry pi.

![](https://github.com/topherCantrell/ER-OLEDM032-1/blob/master/DemoRun.jpg)


