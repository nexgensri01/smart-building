# SmartCitiesIoT Exercise Group 16

# + Backend
Backend consists of below docker services
* Mosquitto - MQTT broker
* Telegraf - Configured to subscribe to a topic and upload the received data into influxDB
* InfluxDB - Time Series Database to store history of collected sensor data
* Grafana - Used to Visualize the data store in influxDB

# + Data Processing
Consits of python scripts to process the data from MQTT/Google Caledar API and make decisions to reach configured goals

# + RaspberryPI
Below sensors are connected to the RaspberryPi 3B+
* Light Sensor
* Temperature/Humidity Sensor (DHT11)
* PIR Sensor
* BME680 Sensor(Indoor Air quality)

Actuators:
* Plugwise stick(Controls two plugwise circles)
* LCD Display
* LED 

Services running in RPi:
* Python script for sensor data collection and publishing - Data is collected from sensors connected to GrovePi+ and publish to MQTT broker
* Python script to enable REST Api server to control the actuators. (This script also provies REST Api to collect sensor data)
* Python script to collect indoor-air-quality from BME680
