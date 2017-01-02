import smbus
import time
import Adafruit_CharLCD as LCD
import subprocess
import urllib2
import os
import sys
import json
import httplib
import codecs

bus = smbus.SMBus(1)
dev_addr = 0x41
lcd = LCD.Adafruit_CharLCDPlate()

################ Configuration ##################
# 15 - RST - 0 (Normal Op)
# 14 - Reserved - 0
# 13 - Heater En - 0 (Disable)
# 12 - Acq Mode - 0 (Temp or Hum)
# 11 - Battery - 0 ( > 2.8V)
# 10 - T resolution - 0 (14bit)
# 9:8 - H resolution - 10 (8bit)
# 7:0 - Reseverd -0 
#################################################

#Set the configuratino
bus.write_byte(dev_addr,0x02)
bus.write_byte(dev_addr,0x02)
bus.write_byte(dev_addr,0x00)

while True:
        if lcd.is_pressed(LCD.SELECT):
        	# Button is pressed, voice recognition starts.
		subprocess.call('./voice_conv.sh', shell=True)
	
		# Send the FLAC file and Receive the response
		url = "https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyCOV8D3c9oLK4w2ExmVFCCsTq_y_yCMItk"
		audio = open('voice.flac','rb').read()
		headers={'Content-Type': 'audio/x-flac; rate=16000', 'User-Agent':'Mozilla/5.0'}
		request = urllib2.Request(url, data=audio, headers=headers)
		time.sleep(1)
		response = urllib2.urlopen(request)
		time.sleep(1)

		# Process the response
		r = response.read()
		r = r.split('\n', 1)[1]
		print r.decode('utf-8')
		res = json.loads(r)['result'][0]['alternative'][0]['transcript']
		
		if ("temperature" or "Temperature") in res :
			print 'YEAH!'
			#Read Temperature
			bus.write_byte(dev_addr,0x00)

			time.sleep(0.015)
			temp = bus.read_byte(dev_addr) #For now, only 8 bits.

			#Calculate & Print Temperature
			print temp
			temp_abs = temp / 256.0 * 165.0 - 40
			print 'The temperature now is %.2f' % (temp_abs)
			time.sleep(3.0)
			
			lcd.set_color(1.0, 0.0, 0.0)
			lcd.clear()
			lcd.message('Temp : %.2f\'C' % (temp_abs))
			time.sleep(3.0)

		elif ("humidity" or "Humidity") in res:
			#Read Humidity
			bus.write_byte(dev_addr, 0x01)
			time.sleep(0.015)
			hum = bus.read_byte(dev_addr)

			#Calculate & Print Humidity
			print hum
			hum_per = hum *100.0 /256.0;
			print 'The humidity now is %.2f%%.' % (hum_per)

			lcd.set_color(1.0, 0.0, 0.0)
			lcd.clear()
			lcd.message('Humidity : %.2f%%' % (hum_per))
			time.sleep(3.0)

		else :
			lcd.set_color(1.0, 0.0, 0.0)
			lcd.clear()
			lcd.message('I cannot understand')
			time.sleep(3.0)
	else :
		lcd.set_color(1.0, 0.0, 0.0)
		lcd.clear()
		lcd.message('Press select')
		#time.sleep(0.2)
	
