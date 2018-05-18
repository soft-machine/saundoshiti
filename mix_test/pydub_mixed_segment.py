#example of mixing a segment of sounds randomly
from pydub import AudioSegment
import random
import dircache
import os
from pydub.playback import play
from time import sleep

dir = '/home/pi/audio_files/test/'

#initialize variables
sounds = []
pos_x = []
mixed = []
count = 10
mix_length = 11000
#mixed = AudioSegment.silent(duration=10000)

try:
	while count < 50:
		for x in range(count):
			if x == 1:
				""" 
				Here we declare our final mixed clip duration.
				To avoid confusion, overlay function in pydub uses first sound clip
				to determine the permitted length for all following sound clips
				"""
				sounds.append(AudioSegment.silent(duration=mix_length))
			else:
				filename = random.choice(dircache.listdir(dir))
				print "file is ",filename 
				path = os.path.join(dir, filename)

				clip_length = len(AudioSegment.from_wav(path))
				cutoff = mix_length - clip_length
				pos_x.append(random.randint(0, cutoff))
				sounds.append(AudioSegment.from_wav(path))

		mixed = sounds[1].overlay(sounds[2])

		pos_count = 0
		for sound in sounds:
			try:
				x_int = pos_x[pos_count]
			except IndexError: 
				pass
			mixed = mixed.overlay(sound, position=x_int)
			pos_count += 1
				
		play(mixed)
		count += 1
		del sounds[:] # clear all list of sounds
		del pos_x[:]
		print "count is ",count
		# save file
		#mixed.export("mixed_",count,".wav" format='wav') # export mixed  audio file

except KeyboardInterrupt:
	print " " 
	print "script terminated. goodbye!"
	exit(0)
