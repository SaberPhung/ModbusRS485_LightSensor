import time
import json
import sys
import datetime
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import vts
from iotticket.models import datanodesvalue
from iotticket.client import Client

data = json.load(open("demo/config.json"))
username = data["username"]
password = data["password"]
deviceId = data["deviceId"]
baseurl = data["baseurl"]

while 1:
	#create client object
	c = Client(baseurl,username,password)	
	#read the content of the sensor
	tempfile = open("/sys/bus/w1/devices/28-000006b19b27/w1_slave")
	text = tempfile.read()
	tempfile.close()
	#split to get the second line temperature data
	tempdata = text.split("\n")[1].split(" ")[9]
	#get the actual number of the temperature
	temperature = float(tempdata[2:])
	#divided by 1000 to get real temperature degree
	temperature = temperature/1000
	#create datanodesvalue object and call the set functions
	nv = datanodesvalue()
	nv.set_name("Sensor temperature")
	nv.set_path("tempVal")
	nv.set_dataType("double")
	nv.set_unit("deg")
	#set the value of the node with the temperature value
	nv.set_value(temperature)
	#set the timestamp as now
	nv.set_timestamp(c.dttots(datetime.datetime.now()))
	#call writedata function
	c.writedata(deviceId, nv)
	print("v: " + str(nv.get_value()) +"\nts: " + str(nv.get_timstamp()) + "\n")
	#the program will run every 2 seconds
	time.sleep(2)
