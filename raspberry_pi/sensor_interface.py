#!/usr/bin/env python
import time
import grovepi
import math
import paho.mqtt.client as paho
import pickle


# sensor_interface.py
# Functions to read sensor data on request.

##Ports to which the devices are connected.
dht_sensor_port = 4  # The Sensor goes on digital port 4.
pir_sensor_port = 8
light_sensor_port = 0


##Sensor configurations
# temp_humidity_sensor_type - DHT11 (1Hz measuring interval)
dht11 = 0    # The Blue colored sensor.

grovepi.pinMode(pir_sensor_port,"INPUT")
grovepi.pinMode(light_sensor_port,"INPUT")

##Varialbes
motion=0
client1= paho.Client("sensors1")                           #create client object
fp = open("shared.pkl","r")

while True:
    try:
        print(" ")
        # Sense Temprature and Humidity
        [temp,humidity] = grovepi.dht(dht_sensor_port,dht11)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
        # Sense motion, usually human, within the target range
        motion=grovepi.digitalRead(pir_sensor_port)
        if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
            if motion==1:
                print ('Motion Detected')
            else:
                print ('-')
        sensor_value = grovepi.analogRead(light_sensor_port)
        sensor_value = sensor_value/8 #change it to relative percentage
        print("Light intensity = %d" % (sensor_value))
        try:
            shared = pickle.load(fp)
            print("IAQ = %f" %(shared["iaq"]))
        except EOFError:
            print("IAQ Error")
            shared = {"iaq": 0}

        client1.connect("192.168.1.101",1883)                                 #establish connection

	client1.publish("u38/0/353/temperature/1","u38/0/353/ temperature="+str(temp))                   #publish
	client1.publish("u38/0/353/humidity/1","u38/0/353/ humidity="+str(humidity))                   #publish
	client1.publish("u38/0/353/presense/1","u38/0/353/ presense="+str(motion))                   #publish
	client1.publish("u38/0/353/light/1","u38/0/353/ light="+str(sensor_value))                   #publish
	client1.publish("u38/0/353/iaq/1","u38/0/353/ iaq="+str(shared["iaq"]))                   #publish
        client1.disconnect()
        time.sleep(30)
    except IOError:
        print ("MQTT post Error. Attempt to reconnect in sometime")
        client1.disconnect()
        time.sleep(30)
