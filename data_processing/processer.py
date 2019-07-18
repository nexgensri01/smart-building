#!/usr/bin/python
#
import paho.mqtt.client as mqtt
import requests 
import pyowm

temperature_desired=27.02
humidity_desired=50
light_desired=70
iaq_desired=50
outdoor_temperature = 0
minimum_temperature_range = temperature_desired - 2
maximum_temperature_range = temperature_desired + 2
weathercode = 0

actuator_url="http://192.168.1.100:3030"
meeting_room=actuator_url+"/meeting"
normal_room=actuator_url+"/353"

def on_message_weather_forecast():
    global outdoor_temperature
    global weathercode
    stuttgart_cityID = 3220785
    owm = pyowm.OWM('d908b571ca6ddb0814c1940fdcaa7324')
    observation = owm.weather_at_id(3220785)
    weather_report = observation.get_weather()
    outdoor_temperature = weather_report.get_temperature('celsius')['temp']
    weathercode = weather_report.get_weather_code()

def on_message_temp(mosq, obj, msg):
#    print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    tag,value = msg.payload.split("=")
    on_message_weather_forecast()
    print("Temp = "+value)
    print("Outdoor temperature="+(str(outdoor_temperature)))
    if(float(value) < temperature_desired):
        if (outdoor_temperature <= maximum_temperature_range) and (outdoor_temperature >= temperature_desired):
            if weathercode not in range(200, 623):
                print("Open Windows")
                requests.get(normal_room + "/window" + "/on")
                requests.get(normal_room + "/ac" + "/off")
                requests.get(normal_room + "/heater" + "/off")
        else:
            print("Close Windows")
            requests.get(normal_room + "/window" + "/off")
            requests.get(normal_room + "/heater" + "/on")
    elif(float(value) > temperature_desired):
        if(outdoor_temperature >= minimum_temperature_range) and (outdoor_temperature <= temperature_desired):
            if weathercode not in range(200, 623):
                print("Open Windows")
                requests.get(normal_room + "/window" + "/on")
                requests.get(normal_room + "/ac" + "/off")
                requests.get(normal_room + "/heater" + "/off")
        else:
            print("Close Windows")
            requests.get(normal_room + "/window" + "/off")
            requests.get(normal_room + "/ac" + "/on")
    else:
        print("Room is at desired temperature")
        requests.get(normal_room + "/ac" + "/off")
        requests.get(normal_room + "/heater" + "/off")

def on_message_humidity(mosq, obj, msg):
#    print("BYTES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    tag,value = msg.payload.split("=")
    print("Humidity = "+value)
    if float(value)<humidity_desired:
        requests.get(normal_room+"/vent"+"/off")
        print("Turn OFF Ventilator ")
    elif float(value)>humidity_desired:
        requests.get(normal_room+"/vent"+"/on")
        print("Turn ON Ventilator")
    else:
        print("Room is in desired Humidity")
        requests.get(normal_room+"/vent"+"/off")

def on_message_iaq(mosq, obj, msg):
#    print("BYTES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    tag,value = msg.payload.split("=")
    print("IAQ = "+value)
    if float(value)<iaq_desired:
        print("Indoor Air quality is good")
        requests.get(normal_room+"/iaqwarn"+"/off")
    elif float(value)>iaq_desired:
        requests.get(normal_room+"/iaqwarn"+"/on")
        print("Indoor Air quality is POOR WARN user")
    else:
        print("Room AirQuality is good")

def on_message_light(mosq, obj, msg):
#    print("BYTES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    tag,value = msg.payload.split("=")
    print("Relative Light Intensity = "+value)
    if int(value)<light_desired:
        print("Increase Light Brightness")
        requests.get(normal_room+"/light"+"/on")
    elif int(value)>light_desired:
        print("Decrease Light Brightness")
        requests.get(normal_room+"/light"+"/off")
    else:
        print("Room is in optimal light level")

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
mqttc.message_callback_add("u38/0/353/temperature/#", on_message_temp)
mqttc.message_callback_add("u38/0/353/humidity/#", on_message_humidity)
mqttc.message_callback_add("u38/0/353/iaq/#", on_message_iaq)
mqttc.message_callback_add("u38/0/353/light/#", on_message_light)
mqttc.on_message = on_message
mqttc.connect("192.168.1.101", 1883)
mqttc.subscribe("#", 2)

mqttc.loop_forever()
