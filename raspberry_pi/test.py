import RPi.GPIO as GPIO
import requests

def button_callback(channel):
	URL = "http://ec2-52-38-69-34.us-west-2.compute.amazonaws.com:80/api/v1/test"
	print("Button was pushed!")
	DATA = {'has_moisture': True}
	r = requests.post(url = URL, data = DATA)
	print(r.text)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(21,GPIO.RISING,callback=button_callback,bouncetime=1000)

message = input("Press enter to quit\n\n")

GPIO.cleanup()
