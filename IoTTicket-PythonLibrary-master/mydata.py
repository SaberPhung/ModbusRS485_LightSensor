#lib
import serial
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

#main

device ='COM6'
arduino = serial.Serial(device, 9600)
list_value=[]
list_in_floats=[]
#data = json.load(open(sys.argv[1]))
data = json.load(open("demo/config.json"))
username = data["username"]
password = data["password"]
deviceId = data["deviceId"]
baseurl = data["baseurl"]

c = Client(baseurl, username, password)


def send_data_to_iot_ticket(value,value2):
    print("WRITE DEVICE DATANODES FUNTION.")
    listofvalues=[]
    nv = datanodesvalue()
    nv.set_name("Humidity") #needed for writing datanode
    nv.set_path("hum")
    nv.set_dataType("double")
    nv.set_unit("Hum")
    nv.set_value(value) #needed for writing datanode
    nv1 = datanodesvalue()
    nv1.set_name("Temperature") #needed for writing datanode
    nv1.set_path("temp")
    nv1.set_dataType("double")
    nv1.set_unit("Temp")
    nv1.set_value(value2) #needed for writing datanode
    listofvalues.append(nv)
    listofvalues.append(nv1)
    print(c.writedata(deviceId, *listofvalues)) # another way to make this would be c.writedata(deviceId, nv, nv1)
    print("END WRITE DEVICE DATANODES FUNCTION")
    print("-------------------------------------------------------\n")

try:
    while True:
        data = arduino.readline()
        decoded=str(arduino[0:len(arduino)].decode("utf-8"))
        list_value=decoded.split(" ")
        try:
            for item in list_value:
                list_in_floats.append(float(item))
        except:
            print('can not float data')
    value=list_in_floats[0]
    value2=list_in_floats[1]
    send_data_to_iot_ticket(value,value2);
    time.sleep(10)

except:
        print('can not open arduino')
    
