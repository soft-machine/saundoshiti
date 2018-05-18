# saundoshiti
student project uses multiple RC522 RFID readers on a single raspberry pi

The codes were built upon the classes originally available here: https://github.com/mxgxw/MFRC522-python

The file MFRC522.py is only slightly changed to not include the activation of NRSTPD (MFRC522 reset pin).
By changing this pin's state directly in the code we are able to switch between several different RFID readers.
The RST pin on all inactive cards must be set LOW. Only one at a time may be set HIGH so as to read it without disturbance from the other connected readers.

Pydub is being used to read audio files as response to RFID tag recognition. Run the following in terminal to install:
"pip install pydub"

The final code (4_modules_final.py) is prepared using pygame instead of pydub. We needed to run multiple channels of sound at arbitrary moment. For the sake of efficiency the pygame module offered this possibility without too much research time required.

The following information is modified from the readme file provided by mxgxw.
read, write, and dump data from a chip

MFRC522-python
==============
Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
 
A small class to interface with the NFC reader Module MFRC522 on the Raspberry Pi.
This is a Python port of the example code for the NFC module MF522-AN.

## Requirements
This code requires you to have SPI-Py installed from the following repository:
https://github.com/lthiery/SPI-Py

## Examples
This repository includes two separate codes to manage sound response using 2 separate ID tags and numerous RFID modules. The final code titled "3_module_audio_response.py" is best commented as this was our final goal.

## Pins

All readers are connected to the same following pins
Only the RST pin is different for each

| Name | Pin # | Pin name   |
|:------:|:-------:|:------------:|
| SDA  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| IRQ  | None  | None       |
| GND  | Any   | Any Ground |
| 3.3V | 1     | 3V3        |

=== RST pins per reader (A,B,C) ===

| Name | Pin # | Pin name   |
|:------:|:-------:|:------------:|
| RST_A| 15    | GPIO22     |
| RST_B| 18    | GPIO24     |
| RST_C| 22    | GPIO25     |

## License
This code and examples are licensed under the GNU Lesser General Public License 3.0.

