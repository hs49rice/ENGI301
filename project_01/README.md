# Clap-on LED Lightstrip

## Build Instructions

### Hardware
1. USB Mini Microphone
Before inserting the Pocketbeagle on the breadboard, breadboard wires should be inserted ahead of time for the 5pin micro USB port. Wires should be placed so that when P1_1 of the Pocketbeagle is inserted into hole 1a of the breadboard:
- P1_7 is connected to VCC of the USB port
- P1_9 is connected to D- of the USB port
- P1_11 is connected to D+ of the USB port
- P1_13 is connected to ID of the USB port
- ID and GND of the USB port should both be connected to each other

The micro USB to USB A adapter should then be inserted into the port followed by the USB A mini microphone. The Pocketbeagle can now also to inserted into the breadboard, where P1_1 would be inserted into hole 1a of the breadboard.

2. Power Bussing
To provide power through the breadboard, the Pocketbeagle must be wired so that power can go through the power bus rails on either side of the breadboard. Using jumper wires:
- Connect P1_14 to the "+" power bus rail of the breadboard, this will provide 3.3 V through the rail
- Connect P1_16 to the "-" power bus rail of the breadboard, this will be the ground rail

The rails on either side of the breadboard should also be connected together so that both sets of rails share the same power and ground.

3. Push Buttons
The three push buttons will be used to switch between the three color pattern settings. They must be inserted in the middle of the breadboard so that the plastic nubs on the bottom fit into the groove at the center of the breadboard. A 1k Ohm resistor should be connected to the "+" power bus and one of the button terminals. A jumper wire should also be connected between the resistor and same button terminal to a GPIO pin on the Pocketbeagle. The other button terminal should be grounded by connecting it to the "-" rail of the breadboard using a jumper wire. Repeat the same steps for the other two buttons. I used P2_2, P2_4, and P2_6 for my GPIO pins.

4. LED Strip and Level Shifter
To use connect the LED strip you must first connect the USB power hub to an outlet. The USB to 5pin terminal block can then be inserted into the USB hub. The level shifter will be inserted into the middle of the breadboard next to the push buttons. Connections are as follows:
- "+" port of the 5pin terminal block to VB pin
- "-" port of the 5pin terminal block to ground "-" rail
- VA pin to OE pin
- VA pin to 3.3 V "+" power rail
- A1 pin to P1_8 on Pocketbeagle

Using jumper cables the LED strip can also be connected to the level shifter.
- The 5V (red) wire of the LEDs will be connected to VB pin of the level shifter.
- The Data In (green) wire of the LEDs will be connected to the B1 pin of the level shifter.
- The ground (white) wire of the LEDs will be connected to the ground rail of the breadboard.

### Software
1. USB Mini Microphone Set-up
To set up the usb microphone, first run these sets of commands in Cloud9:
```
sudo apt-get update
sudo apt-get install -y swig libpulse-dev libasound2-dev
```
Once finished, run command:
```
arecord -l
```
Once ran, make note of the device number and card number. Then run command:
```
nano ~/.asoundrc
```
You should see in the terminal `pcm "hw:#, #"` The first number should correspond to your card number, followed by your device number. If they do not match, edit the text accordingly. Once this is complete, your microphone should now be set up.

2. LED Strip Set-up
For the LED strip, first download and put the following files into a directory:
- configure_pins.sh
- run
- run-opc-server
- opc-server
- opc.py
- config.json
- project.py

Note that configure_pins.sh, run, run-opc-server, opc-server must be given permissions 755. This can be done by running:
```
chmod 755 configure_pins.sh opc-server run run-opc-server
```
You can check if this successfully worked by running command `ls -l` and checking to see if the files are highlighted green.
Also, the following PRU files must be in a subdirectory pru/bin/:
- pru/bin/ws281x-original-ledscape-pru0.bin
- pru/bin/ws281x-original-ledscape-pru1.bin

We then must the following command to edit uENv.txt:
```
sudo nano /boot/uEnv.txt
```
Once the textbox appears, comment out the RPROC firmware and uncomment the UIO firmware.
Once that is complete run commands `sudo reboot` and `ls /sys/class/uio` to check that UIO is available.

## Operation

First plug the USB hub into an outlet. Make sure you press the button on the USB hub to send power to your LED light strip. A micro USB to USB A cable should be used to connect the Pocketbeagle to your laptop.
Two terminals must be used to run the code. The command:
```
sudo ./run-opc-server
```
should be entered into the first terminal to run the server. Then, the command:
```
./run
```
should be entered into the second terminal to run the main code. Once the commands are initialized, all of the LEDs in the strip should be completely off. Clap your hands to turn on the LEDs. They should all be turned on colored white. Once the LED lights are on, you can change the color settings by pressing the buttons on the breadboard. Pressing the push button connected to P2_2 will set the LEDs to the warm colors mode. Pressing the push button connected to P2_4 will set the LEDs to the cool colors mode. Pressing the push button connected to P2_6 will set the LEDs to the rainbow colors mode. You can clap again while the LEDs are on to turn the LED strip off.

More detailed instructions can be found at the following link: https://www.hackster.io/hs49/clap-on-led-light-strip-6bed85




