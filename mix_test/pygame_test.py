import pygame
from time import sleep
# Initialize the mixer
pygame.mixer.init()
# Load two sounds
snd1 = pygame.mixer.Sound('/home/pi/audio_files/final/banque.wav')
snd2 = pygame.mixer.Sound('/home/pi/audio_files/final/hopital.wav')
# Play the sounds; these will play simultaneously
snd1.play()
snd2.play()
for x in range(0, 3):
        print "We're on time %d" % (x)
        sleep(1)
exit()
