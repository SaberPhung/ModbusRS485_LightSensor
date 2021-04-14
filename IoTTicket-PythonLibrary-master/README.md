# IoT-Ticket Python client

IoT-Ticket Python client provides an easy-to-use library and examples so that your application can take advantage of the versatile IoT-Ticket cloud tools.

## System requirements
<pre><code>
This Python library required Python 3 installed in your system.
Lastest version of Python could be downloaded from: https://www.python.org/downloads/
When Python installation file is downloaded, It could be installed into the system like normal program
</code></pre>
## Getting started
<pre><code>
1. This Python library required Python 3 installed in your system.
2. Create your own IoT-Ticket account at https://www.iot-ticket.com/ (Request an invitation)
3. Wait for the account activation email
4. Download library from github.
5. Extract the Zip file, point Pythonpath to the directory that contain the library.
6. Start using the library in your application.
</code></pre>
### Using the library

In your application, import the needed libraries
<pre><code>
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client
</code></pre>
The iotticket.client is the main library to be used. All the rest above is used to create objects of its class.

### Provided funtion in client

Here are the list of provided functions
<pre><code>
getdevice(self, deviceId)
getdevices(self, limit, offset)
getdatanodeslist(self, deviceId, limit, offset)
getallquota(self)
getdevicequota(self, deviceId)
registerdevice(self, deviceobj)
movedevice(self, deviceId, enterpriseId)
readdata(self, deviceId, criteriaobj, fromdate, todate, limit)
writedata(self, deviceId, *datanodevalueobj)
</code></pre>
### Example code
The library contains a demo which provides a complete example application. Also, the unit tests can be used as a reference.
demo/demo.py
test/unittest.py
NOTE: In order to run the demo application or unittest provided in our project, you need to create yourself a config.json file.
<pre><code>
{
    "username": "your_username",
    "password": "your_password",
    "deviceId": "your_deviceId",
    "baseurl": "https://my.iot-ticket.com/api/v1/"
}
</code></pre>
NOTE: The base URL if you are using basic IoT-Ticket server will be: "https://my.iot-ticket.com/api/v1/"
In demo application, config file is called:
<pre><code>
data = json.load(open(sys.argv[1]))
username = data["username"]
password = data["password"]
deviceId = data["deviceId"]
baseurl = data["baseurl"]
</code></pre>
The examples could be run by using command. You need to provide command line argument which point to your config file:
<pre><code>
$ python file_name.py path_to_your_config_file
</code></pre>
### Verify or Unverify Certificate
<pre><code>
c = Client(baseurl, username, password, False)
</code></pre>
True is default if no argument is given. If False is given, the unverified mode will be on. It will not check url certificate.
### Registering a device
<pre><code>
d = device()
d.set_name("Johan")
d.set_manufacturer("Wapice")
d.set_type("employee")
d.set_description("Im trainee")
d.set_enterpriseId("E0000")
d.set_attributes(deviceattribute("a","b"), deviceattribute("c","d"), deviceattribute("key","value")) [replace the arguments by list of deviceattribute object]	

c = client(baseurl, username, password)

c.registerdevice(d)
</code></pre>
Register Device Function source code:
<pre><code>
    def registerdevice(self, deviceobj):
        """Register new device."""
        if (validate(deviceobj)):
            try:
                # parse to json and encode
                device_dict = deviceobj.__dict__
                enterprise = device_dict["enterpriseId"]
                print(device_dict)
                if enterprise == "":
                    device_dict.pop("enterpriseId")
                j = json.dumps(device_dict, sort_keys=True, indent=4)
                data = j.encode("utf8")
                pathUrl = self.baseUrl + self.deviceresource

                req = urllib.request.Request(pathUrl,data=data, headers=self.headers)

                with urllib.request.urlopen(req, context=self.context) as response:
                    response = response.read()

            except err.HTTPError as e:
                raise self.get_errorinfo(e.code, e.read()) from None
            else:
                return self.get_response(response, "iotticket.models.device")
        else:
            return "Device is not valid."
</code></pre>

### Move a device
<pre><code>
c = client(baseurl, username, password)

c.movedevice(deviceId,"E0001")

parameters of movedevice are device id of device that is moved and enterprise id of destination enterprise.
</pre></code>
### Validate function
Validate function using declared criteria in class
<pre><code>
crit = [{"name": {"max_length":100, "nullable" : False}}, {"unit": {"max_length": 10}}, {"path": {"max_length": 1000, "regex" : "(\\/[a-zA-Z0-9]+){1,10}"}}]
</code></pre>
Validation code:
<pre><code>
import re
def validate(obj):
	isValid = True
	for n in obj.crit:
		for key in n:
			critlist = n[key]
			for critlistkey in critlist:
				if critlistkey == "max_length":
					if len(getattr(obj,key)) > critlist[critlistkey]:
						isValid = False
				if critlistkey == "nullable":
					if critlist[critlistkey] is False:
						if(getattr(obj,key) == "" or getattr(obj,key) == None or getattr(obj,key) == 0):
							isValid = False
				if critlistkey == "regex":
					if( not re.match(critlist[critlistkey], getattr(obj,key), flags = 0)):	
						isValid = False
				if critlistkey == "dataType":
					if not isinstance(getattr(obj,key), critlist[critlistkey]):
						isValid = False
	return isValid		
</code></pre>			
### Sending data
<pre><code>
nv = datanodesvalue()
nv.set_name("Finger No")
nv.set_path("fingerno")
nv.set_dataType("double")
nv.set_value(10)	

c = client(baseurl, username, password)

c.writedata(deviceId, nv)
</code></pre>
### Get datanodes for a device
<pre><code>
c = client(baseurl, username, password)

c.getdatanodeslist(deviceId, 10, 0)
</code></pre>
### Read data
<pre><code>
cr = criteria()
cr.set_criterialist("Latitude", "Longitude") [Replace the arguments by your criteria, separate by ","]

c = client(baseurl, username, password)
fd = "2016-03-22 17:22:00"
td = "2016-03-22 17:25:00"

c.readdata(deviceId, cr, fd , td, limit)

fromdate and todate is not required. it can be set and passed as argument.
If limit is provided but not fromdate and todate, then the function can be called as c.readdata(deviceId, cr, "", "", limit)
If no extra argument is provided, simply call c.readdata(deviceId, cr)
</code></pre>
## API documentation
This Python client library uses the IoT-Ticket REST API. The documentation for the underlying REST service can be found from
https://www.iot-ticket.com/images/Files/IoT-Ticket.com_IoT_API.pdf
