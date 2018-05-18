#!/usr/bin/env python
# -*- coding: utf8 -*-

import pygame
from subprocess import call
import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep

continue_reading = True
myVolume = 0.5

#this list designates our 4 RFID readers by the RPi pins to which each RST is connected
rstPins=[15,18,22,38]
#make a counter and start at 0
rstCount = 0;
countLimit=len(rstPins)

#setup our hardware RST pins and set them low to begin
GPIO.setmode(GPIO.BOARD)
for i in range(len(rstPins)):
    GPIO.setup(rstPins[i], GPIO.OUT)
    GPIO.output(rstPins[i], 0)

# Initialize pygame mixer
pygame.mixer.init(frequency=22050,size=-16,channels=2,buffer=4096)

#audio files. change for wherever you place them in the system
snd1 = pygame.mixer.Sound("/home/pi/audio_files/final/banque.wav")
snd2 = pygame.mixer.Sound("/home/pi/audio_files/final/conservatoire.wav")
snd3 = pygame.mixer.Sound("/home/pi/audio_files/final/hopital.wav")
snd4 = pygame.mixer.Sound("/home/pi/audio_files/final/hotel.wav")

alt1 = pygame.mixer.Sound("/home/pi/audio_files/final/alt_banque.wav")
alt2 = pygame.mixer.Sound("/home/pi/audio_files/final/alt_conservatoire.wav")
alt3 = pygame.mixer.Sound("/home/pi/audio_files/final/alt_hopital.wav")
alt4 = pygame.mixer.Sound("/home/pi/audio_files/final/alt_hotel.wav")

ch1 = pygame.mixer.Channel(0)
ch2 = pygame.mixer.Channel(1)
ch3 = pygame.mixer.Channel(2)
ch4 = pygame.mixer.Channel(3)
ch1a = pygame.mixer.Channel(4)
ch2a = pygame.mixer.Channel(5)
ch3a = pygame.mixer.Channel(6)
ch4a = pygame.mixer.Channel(7)

citysound = pygame.mixer.Sound("/home/pi/audio_files/final/ville.wav")
citysound.play(loops=-1)

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

    #activate RFID reader and initiate
    GPIO.output(rstPins[rstCount], 1)
    MIFAREReader.MFRC522_Init()

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        """
        if rstCount == 0:
            call(["espeak","-s140 -ven+18 -z","Module 1"])
        elif rstCount == 1:
            call(["espeak","-s140 -ven+18 -z","Module 2"])
        elif rstCount == 2:
            call(["espeak","-s140 -ven+18 -z","Module 3"])
	elif rstCount == 3:
            call(["espeak","-s140 -ven+18 -z","Module 4"])
        """
        cardID = str(uid[3])
        print "card ID is", cardID
        if int(cardID) == 185 and rstCount == 0:
            if not ch1.get_busy():
                ch1.play(snd1)
                ch1.set_volume(myVolume)

        elif int(cardID) == 185 and rstCount != 0:
            if not ch1a.get_busy():
                ch1a.play(alt1)
                ch1a.set_volume(myVolume)

        if int(cardID) == 41 and rstCount == 1:
            if not ch2.get_busy():
                ch2.play(snd2)
                ch2.set_volume(myVolume)

        elif int(cardID) == 41 and rstCount != 1:
            if not ch2a.get_busy():
                ch2a.play(alt2)
                ch2a.set_volume(myVolume)

        if int(cardID) == 89 and rstCount == 2:
            if not ch3.get_busy():
                ch3.play(snd3)
                ch3.set_volume(myVolume)

        elif int(cardID) == 89 and rstCount != 2:
            if not ch3a.get_busy():
                ch3a.play(alt3)
                ch3a.set_volume(myVolume)

	if int(cardID) == 163 and rstCount == 3:
            if not ch4.get_busy():
                ch4.play(snd4)
                ch4.set_volume(myVolume)

        elif int(cardID) == 163 and rstCount != 3:
            if not ch4a.get_busy():
                ch4a.play(alt4)
                ch4a.set_volume(myVolume)

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
