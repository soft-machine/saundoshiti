from subprocess import call
import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep
from pydub import AudioSegment
from pydub.playback import play

continue_reading = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, 0)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, 1)

audio1 = AudioSegment.from_file("/home/pi/audio_files/cow.wav")
audio2 = AudioSegment.from_file("/home/pi/audio_files/cricket.wav")

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
myFlag = 0
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    #to change for a better method
    if myFlag == 0:
        GPIO.output(15, 0)
        GPIO.output(22, 1)
        myFlag = 1
        MIFAREReader.MFRC522_Init()
    elif myFlag == 1:
        GPIO.output(15, 1)
        GPIO.output(22, 0)
        myFlag = 0
        MIFAREReader.MFRC522_Init()

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        print "card is #", myFlag
        if myFlag == 0:
            call(["espeak","-s140 -ven+18 -z","Module 1"])
        elif myFlag == 1:
            call(["espeak","-s140 -ven+18 -z","Module 2"])

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

