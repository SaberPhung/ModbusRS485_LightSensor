#lib
import json
import sys
import time
import random
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client

#main

#data = json.load(open(sys.argv[1]))
data = json.load(open("demo/config.json"))
username = data["username"]
password = data["password"]
deviceId = data["deviceId"]
baseurl = data["baseurl"]

c = Client(baseurl, username, password)

def send_data_to_iot_ticket(value,value2,value3,value4):
    print("WRITE DEVICE DATANODES FUNTION.")
    listofvalues=[]
    nv = datanodesvalue()
    nv.set_name("Humidity") #needed for writing datanode
    nv.set_path("hum")
    nv.set_dataType("double")
    nv.set_unit("Hum")
    nv.set_value(value) #needed for writing datanode
    nv.set_timestamp(time.time()*1000)
    nv1 = datanodesvalue()
    nv1.set_name("Temperature") #needed for writing datanode
    nv1.set_path("temp")
    nv1.set_dataType("double")
    nv1.set_unit("Temp")
    nv1.set_timestamp(time.time()*1000)
    nv1.set_value(value2) #needed for writing datanode
    nv2 = datanodesvalue()
    nv2.set_name("Carbondioxide") #needed for writing datanode
    nv2.set_path("carbon")
    nv2.set_dataType("double")
    nv2.set_unit("Carbon")
    nv2.set_timestamp(time.time()*1000)
    nv2.set_value(value3) #needed for writing datanode
    nv3 = datanodesvalue()
    nv3.set_name("Oxyzen") #needed for writing datanode
    nv3.set_path("oxyzen")
    nv3.set_dataType("double")
    nv3.set_unit("oxyzen")
    nv3.set_timestamp(time.time()*1000)
    nv3.set_value(value4) #needed for writing datanode
    listofvalues.append(nv)
    listofvalues.append(nv1)
    listofvalues.append(nv2)
    listofvalues.append(nv3)
    print(c.writedata(deviceId,nv,nv1,nv2,nv3)) # another way to make this would be c.writedata(deviceId, nv, nv1)
    print("END WRITE DEVICE DATANODES FUNCTION")
    print("-------------------------------------------------------\n")

while True:
    #write datanode demo
    value=random.uniform(0,100)
    value2=random.uniform(-30,50)
    value3=random.uniform(0,100)
    value4=random.uniform(0,100)
    send_data_to_iot_ticket(value,value2,value3,value4)
    time.sleep(5)
