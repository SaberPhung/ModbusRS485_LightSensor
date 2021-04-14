import json
import sys
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client

data = json.load(open(sys.argv[1]))
username = data["username"]
password = data["password"]
baseurl = data["baseurl"]

#create client object
c= Client(baseurl,username,password)

#create device object and call set functions
d = device()
d.set_name("Raspi Temperature Sensor")
d.set_manufacturer("Wapice")
d.set_type("Sensor")
d.set_description("Temperature sensor")
d.set_attributes(deviceattribute("Sensor model","DS18B20"))
d.set_enterpriseId("E0000") #if enterprise id is not given, iotticket use default enterprise id.
#call registerdevice function
resp = c.registerdevice(d)
#build the new json file for writing data process
data={"username":username,"password":password,"deviceId":resp.get_deviceId(),"baseurl":baseurl}
with open("write.json","w") as outfile:
	json.dump(data, outfile, sort_keys=True, indent=4)
print(resp.get_deviceId())

