import liveapi
import time
import RPi.GPIO as GPIO


# Configuration parameters

GPI_1 = 40 							# GPIO 21
#elemental_ip = '37.157.142.3'
elemental_ip = '192.168.2.3'

# Map GPI inputs to Elemental live streams
gpi2stream = {
		str(GPI_1): '5'
}

# Setup GPIO inputs/outputs
	#Use Board pin numbering - etc. (12) in pinout command
GPIO.setmode(GPIO.BOARD)
	#Setup GPI_1 as the input with PULL-UP
GPIO.setup( GPI_1, GPIO.IN, pull_up_down=GPIO.PUD_UP )





# Define callbacks
state = 0
def start_stop_avail(gpi):
	global state
	print("4. Event detcted")
	
	if GPIO.input(gpi):					# Rising edge == True
		if state == 1:
			print("5. Stopping cue")
			startime = time.time()
			liveapi.cue_command(elemental_ip, gpi2stream[str(gpi)], 'stop_cue')
			print("Reaction time: " + str(time.time() - startime))
			state = 0
			time.sleep(5)
	else:								# Rising edge == False
		if state == 0:
			print("5. Starting cue")
			startime = time.time()
			liveapi.cue_command(elemental_ip, gpi2stream[str(gpi)], 'start_cue')			
			print("Reaction time: " + str(time.time() - startime))
			state = 1
			time.sleep(5)
		
print("1. Init done")
# Tie callbacks to events
GPIO.add_event_detect(GPI_1, GPIO.BOTH, callback = start_stop_avail)
print("2. Event handler added")
try:
	print("3. Waiting for signal")
	while 1:
		pass
		
except KeyboardInterrupt:
	pass
GPIO.cleanup()
		
