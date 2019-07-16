#!/usr/bin/env python
import time
import grovepi
import math
from flask import Flask, render_template, request
from flask_restful import Resource, Api
import pickle 
from plugwise.api import *
from grove_rgb_lcd import *

DEFAULT_PORT = "/dev/ttyUSB0"
mac1 = "000D6F0005670C31"
mac2 = "000D6F0003BD6375"
stick = Stick(DEFAULT_PORT)
circleplus = Circle(mac1, stick)
circle = Circle(mac2, stick)



setText("Init.....")
setRGB(0,128,64)
fp = open("shared.pkl","r")

app = Flask(__name__)
api = Api(app)

# Functions to read sensor data on request.

##Ports to which the devices are connected.
dht_sensor_port = 4  # The Sensor goes on digital port 4.
pir_sensor_port = 8
light_sensor_port = 0
led_port=5


##Sensor configurations
# temp_humidity_sensor_type - DHT11 (1Hz measuring interval)
dht11 = 0    # The Blue colored sensor.

grovepi.pinMode(pir_sensor_port,"INPUT")
grovepi.pinMode(light_sensor_port,"INPUT")
grovepi.pinMode(led_port,"OUTPUT")

##Varialbes
motion=0
on_state="ON "
off_state="OFF"
heater_state=off_state
ac_state=off_state
ventilator_state=off_state
light_intensity=off_state

def updateDisplay():
    textToLCD="Heat:"+heater_state+"Vent:"+ventilator_state+"\nAC:"+ac_state+" Light:"+str(light_intensity)
    setText(textToLCD)


class Light(Resource):
    def get(self):
         #[temp,hum] = grovepi.dht(sensor,0)
         sensor_value = grovepi.analogRead(light_sensor)

         # Calculate resistance of sensor in K
         resistance = (float)(1023 - sensor_value) * 10 / sensor_value

         return {'sensor_value' : sensor_value,
                 'resistance' : resistance }

class Temp(Resource):
    def get(self):
        [temp,humidity] = grovepi.dht(dht_sensor_port,dht11)
        if math.isnan(temp) == False and math.isnan(humidity) == False:

         return {'temperature' : temp,
                 'humidity' : humidity }

class Presense(Resource):
    def get(self):
        # Sense motion, usually human, within the target range
        motion=grovepi.digitalRead(pir_sensor_port)
        if motion==0 or motion==1:      # check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
            if motion==1:
                return {'motion' : motion}
            else:
                return {'motion' : motion}

class IAQ(Resource):
    def get(self):
        shared = pickle.load(fp)
        #print("IAQ = %f" %(shared["iaq"]))
        return {'iaq': shared["iaq"]}


@app.route("/<location>/<deviceName>/<action>")
def action(location, deviceName, action):
    global heater_state, ac_state, ventilation_state, light_intensity
    status=False
    if location == '353':
        if deviceName == 'ac':
            if action == "on":
                setRGB(0,0,255)
                ac_state=on_state
                heater_state=off_state
                status=True
            if action == "off":
                setRGB(212, 235, 255)
                ac_state=off_state
                status=True
        if deviceName == 'heater':
            if action == "on":
                setRGB(255,128,0)
                heater_state=on_state
                ac_state=off_state
                status=True
            if action == "off":
                setRGB(212, 235, 255)
                heater_state=off_state
                status=True
        if deviceName == 'vent':
            if action == "on":
                ventilator_state=on_state
                status=True
            if action == "off":
                ventilator_state=off_state
                status=True
        if deviceName == 'iaqwarn':
            if action == "on":
                grovepi.digitalWrite(led_port,1)
                status=True
            if action == "off":
                grovepi.digitalWrite(led_port,0)
                status=True
        if deviceName == 'light':
            if action == "on":
                light_intensity=on_state
                status=True
            if action == "off":
                light_intensity=off_state
                status=True
    

    if location == 'meeting':
        if deviceName == 'projector':
            if action == "on":
                print("Projector ON")
                circleplus.switch_on() 
                status=True
            if action == "off":
                print("Projector OFF")
                circleplus.switch_off() 
                status=True
        if deviceName == 'blind':
            if action == "on":
                print("Blinds open")
                status=True
            if action == "off":
                print("Blinds Close")
                status=True
        if deviceName == 'light':
            if action == "on":
                circle.switch_on() 
                status=True
            if action == "off":
                circle.switch_off() 
                status=True
        
    updateDisplay()
    return {"status": status}

api.add_resource(Temp, '/u38/0/353/temperature/1')
api.add_resource(Presense, '/u38/0/353/presense/1')
api.add_resource(Light, '/u38/0/353/light/1')
api.add_resource(IAQ, '/u38/0/353/iaq/1')

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=3030, debug=False)

