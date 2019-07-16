Folder for Data processing related files

processor.py - Subscribes to MQTT topics. Processes the received data. Calls RESTAPI actuators.
Mqtt topics configured inside this script. Goal parameters configured inside this script.

quickstart.py - Checks google calendar frequently and calls RESTAPI actuators for meeting room automation. 
This script needs 'credentials.json' - Refer 'https://developers.google.com/calendar/quickstart/python'
