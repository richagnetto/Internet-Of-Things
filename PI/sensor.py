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
import web
import MySQLdb

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
#	if True:
#		time.sleep(30)
        	# Button is pressed, voice recognition starts.
	
		print 'YEAH!'
		#Read Temperature
		bus.write_byte(dev_addr,0x00)

		time.sleep(0.015)
		temp = bus.read_byte(dev_addr) #For now, only 8 bits.

		#Calculate & Print Temperature
		print temp
		temp_abs = temp / 256.0 * 165.0 - 40
		print 'The temperature now is %.2f' % (temp_abs)
		time.sleep(0.1)
			
		#Read Humidity
		bus.write_byte(dev_addr, 0x01)
		time.sleep(0.015)
		hum = bus.read_byte(dev_addr)

		#Calculate & Print Humidity
		print hum
		hum_per = hum *100.0 /256.0;
		print 'The humidity now is %.2f%%.' % (hum_per)

		conn=MySQLdb.connect(host="group21.cloudapp.net",user="pi",passwd="raspberry",db="testdb",port=3306)
        	cur=conn.cursor()
        	try:
			cur.execute("insert into temp (temp , humi) values (%s,%s)",(temp_abs,hum_per))
	        	conn.commit()
		except:
			conn.rollback()
		#print count
        	cur.close()
        	conn.close()
		
	else:
		time.sleep(0.1)
	
sys.exit()
