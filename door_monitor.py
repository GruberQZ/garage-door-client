import RPi.GPIO as GPIO
import requests
import datetime
import time
from slackAPI import slackAPI
from logger import Logger

def nextActionTime(action_time, quiet_time):
	hour = action_time.hour
	minute = action_time.minute + quiet_time
	if (minute>60):
		hour+=1
		minute-=60
	return datetime.time(hour, minute)

def mashGarageDoorButton():
	GPIO.output(17, GPIO.LOW)
	time.sleep(0.6)
	GPIO.output(17, GPIO.HIGH)


# Turn off GPIO warnings
GPIO.setwarnings(False)

# Initialize GPIO for garage door communication
# Set numbering scheme to BCM
GPIO.setmode(GPIO.BCM)

# Initialize GPIO17 (Pin 11), which controls the relay
# Should be an output and set high, because relay is active-low
GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)

# Initialize GPIO27, which is connected to one of the magnet sensor wires
# [the other magnet sensor wire is connected to ground on pin 9]
# Should be an input with the pull-up resistor enabled
# When the garage door is open and the magnet is not near the sensor, GPIO27 will be 1
# When the garage door is closed and the magnet is near the sensor, GPIO27 will be 0
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

door_state = "undetermined"
now = datetime.datetime.now()
next_action_time = datetime.time(now.hour, now.minute)
action_in_progress = False

#Create a slack 
slack = slackAPI()
log = Logger("/home/pi", "door_monitor.log")


# Define interrupt functions that trigger when the door opens or closes
def update_door_log(channel):
	
	global door_state
	# Door just opened
	if GPIO.input(27):
		#print(str(timestamp) + ": Door just opened!")
		if (door_state!="open"):
			door_state = "open"
			print("%s: Door just opened!" % (datetime.datetime.now()))
			log.log("Door just OPENED")
			slack.sendMessage("%s: Door just *OPENED*" % (datetime.datetime.now()))
		
	# Door just closed
	else:
		#print(str(timestamp) + ": Door just closed!")
		if (door_state!="closed"):
			door_state = "closed"
			print("%s: Door just closed!" % (datetime.datetime.now()))
			log.log("Door just CLOSED")
			slack.sendMessage("%s: Door just *CLOSED*" % (datetime.datetime.now()))
		

# Configure interrupt for door opening
#Changed bounced from 600 to 2000 on 11-10-2017.  Getting random close events including closed just prior to open
GPIO.add_event_detect(27, GPIO.BOTH, callback = update_door_log, bouncetime = 2000)

# Run infinitely until keyboard interrupt or system shutdown
try:
	print("%s: Ready to detect door state changes..." % (datetime.datetime.now()))
	log.log("Ready to detect door state changes...")
	slack.sendMessage("%s: Ready to detect door state changes..." % (datetime.datetime.now()))
	# Print initial state
	if GPIO.input(27):
		if (door_state!="open"):
			door_state = "open"
			print("%s: Initial door state: open" % (datetime.datetime.now()))
			log.log("Initial door state: open")
			slack.sendMessage("%s: Initial door state: *open*" % (datetime.datetime.now()))
	else:
		if (door_state!="closed"):
			door_state = "closed"
			print("%s: Initial door state: closed" % (datetime.datetime.now()))
			log.log("Initial door state: open")
			slack.sendMessage("%s: Initial door state: *closed*" % (datetime.datetime.now()))
	
	while True:

		#Get the schedule from the cloud app.  For now, we'll hard code this to close at 10 pm
		now = datetime.datetime.now()
		current_time = datetime.time(now.hour, now.minute)

		desired_close_time_start = datetime.time(22,00)

		#Since we poll the cloud for realtime requests every 5 seconds, we need to make sure multiple actions not triggered while the door is moving
		if desired_close_time_start <= current_time and action_in_progress == False:	

			if door_state=="open": 
				action_in_progress = True
				next_action_time = nextActionTime(current_time, 2)
				log.log("Door is open.  Closing it now")
				slack.sendMessage("%s: Door is open.  Closing it now" % (now))
				mashGarageDoorButton()

		if current_time >= next_action_time:
			action_in_progress = False

		"""
		#Get the schedule from the cloud app.  For now, we'll hard code this to close at 10 pm
		desired_close_time_start = datetime.time(22,00)
		desired_close_time_end = datetime.time(23,15)
		now = datetime.datetime.now()
		current_time = datetime.time(now.hour, now.minute)

		if desired_close_time_start <= current_time <= desired_close_time_end:	
			
			if last_notify_time == None:
				last_notify_time = current_time
				print ("%s: First time in the window of desired close timeframe." % (now))
				if door_state=="open": 
					log.log("Door is open.  Closing it now")
					slack.sendMessage("%s: Door is open.  Closing it now" % (now))
					mashGarageDoorButton()

			if last_notify_time!=None and current_time >= next_notify_time(last_notify_time):
				last_notify_time = next_notify_time(last_notify_time)
				print ("%s: Second time in the window of desired close timeframe." % (now))
				if door_state=="open": 
					log.log("Door is still open.  Closing it")
					slack.sendMessage("%s: Door is still open.  Closing it" % (now))
					mashGarageDoorButton()
		#else:
		#	print ("Not within the desired close timeframe (%s - %s)" % (desired_close_time_start, desired_close_time_end))
		"""

		time.sleep(5)
		

#except IOError:
#    print('An error occured trying to read the file.')
    
#except ValueError:
#    print('Non-numeric data found in the file.')

#except ImportError:
#    print("No module found")
    
#except EOFError:
#    print('Why did you do an EOF on me?')

#except KeyboardInterrupt:
#    print('You cancelled the operation.')

#except:
#    print('An error occured.')

finally:
	print("%s: Shutting down..." % (datetime.datetime.now()))
	log.log("Shutting down...")
	slack.sendMessage("%s: Shutting down..." % (datetime.datetime.now()))
	GPIO.cleanup()
