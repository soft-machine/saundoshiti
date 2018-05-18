#!/usr/bin/env python
# -*- coding: utf8 -*-

from subprocess import call
import RPi.GPIO as GPIO
import MFRC522
import signal
from pydub import AudioSegment
from pydub.playback import play

continue_reading = True

#this list designates our 3 RFID readers by the RPi pins to which each RST is connected
rstPins=[15,18,22]
#make a counter and start at 0
rstCount = 0;
countLimit=len(rstPins)

#setup our hardware RST pins and set them low to begin
GPIO.setmode(GPIO.BOARD)
for i in range(len(rstPins)):
    GPIO.setup(rstPins[i], GPIO.OUT)
    GPIO.output(rstPins[i], 0)

#audio files. change for wherever you place them in the system
audio1 = AudioSegment.from_file("/home/pi/audio_files/duck.wav")
audio2 = AudioSegment.from_file("/home/pi/audio_files/cow.wav")

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips
while continue_reading:
    if rstCount < (countLimit-1):
        rstCount+=1
    else:
        rstCount=0

    print "rstCount is ",rstCount

    #activate RFID reader and initiate
    GPIO.output(rstPins[rstCount], 1)
    MIFAREReader.MFRC522_Init()

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        if rstCount == 0:
            call(["espeak","-s140 -ven+18 -z","Module 1"])
        elif rstCount == 1:
            call(["espeak","-s140 -ven+18 -z","Module 2"])
        elif rstCount == 2:
            call(["espeak","-s140 -ven+18 -z","Module 3"])

        # Print UID
        cardID = str(uid[3])
        print "card ID is", cardID

        if int(cardID) == 57:
            play(audio1)
        elif int(cardID) == 171:
            play(audio2)

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"

    #throw last reader RST pin low 
    GPIO.output(rstPins[rstCount], 0)
