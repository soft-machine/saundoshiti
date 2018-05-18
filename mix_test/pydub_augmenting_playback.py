from pydub import AudioSegment
import random
import dircache
import os
from pydub.playback import play
from time import sleep

dir = '/home/pi/audio_files/test/'

#initialize variables
count = 10
myDelay = 2 #start delay at 10 seconds

try:
	while count < 100:
			if count < 10:
				filename = random.choice(dircache.listdir(dir))
				print "file is ",filename 
				path = os.path.join(dir, filename)
				audio = AudioSegment.from_file(path)
				play(audio)
				sleep(myDelay)
				myDelay -= 1

			else:
                                filename = random.choice(dircache.listdir(dir))
				#dir = '/home/pi/audio_files/test/' + str(count) + '.wav'
				#print dir
				#filename = dir
				print "file is ",filename
				path = os.path.join(dir, filename)
				audio = AudioSegment.from_file(path)
				play(audio)

			count += 1


except KeyboardInterrupt:
	print " " 
	print "script terminated. goodbye!"
	exit(0)
