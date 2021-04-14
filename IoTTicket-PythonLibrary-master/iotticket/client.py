# The MIT License (MIT)
#
# Copyright (c) 2016 Wapice Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# lib
import urllib.request as url  # import request
import urllib.error as err
import urllib.parse
import json  # import json
import datetime
import time
import ssl
from pprint import pprint
from iotticket.models import *
from iotticket.parsejson import parsejson
from iotticket.models import errorinfo
from iotticket.models import criteria
from iotticket.exception import ValidAPIParamException
from iotticket.validation import validate
import base64


# main class
class Client(object):
    """ The main client class from which user can call and use the provided functions."""
    deviceresource = "devices/"
    specificdeviceresourceformat = deviceresource + "{}/"
    datanodesresourceformat = specificdeviceresourceformat + "datanodes/"
    writedataresourceformat = "process/write/{}/"
    readdataresourceformat = "process/read/{}/"
    quotaallresource = "quota/all/"
    quotadeviceresourceformat = "quota/{}/"

    def __init__(self, baseUrl, username, password, verify=True):
        self.baseUrl = baseUrl
        self.username = username
        self.password = password
        if verify == False:
            self.context = ssl._create_unverified_context()
        else:
            self.context = None

        usrPass = username+":"+password
        usrPass = usrPass.encode("UTF-8")
        b64auth = base64.b64encode(usrPass)
        authstring = b64auth.decode("UTF-8")
        self.headers={'content-type': 'application/json','Authorization': 'Basic ' + authstring}



    # connection function
    def connect(self, pathUrl, clz):
        """ Function to connect to server with different URL path to get different response"""
        try:
            req = urllib.request.Request(pathUrl, headers=self.headers)

            with urllib.request.urlopen(req, context=self.context) as response:
                response = response.read()

        except err.HTTPError as e:
            raise self.get_errorinfo(e.code, e.read()) from None
        else:
            return self.get_response(response, clz)

    # date time to timestamp
    def dttots(self, dt):
        """ Convert datetime to timestamp."""
        if isinstance(dt, datetime.datetime):
            return int(1000 * (time.mktime(dt.timetuple()) + dt.microsecond * 1e-6))
        if isinstance(dt, str):
            time_formats = "%Y-%m-%d %H:%M:%S.%f_%Y-%m-%d %H:%M:%S_%Y-%m-%d %H:%M_%Y-%m-%d"
            for f in time_formats.split('_'):
                try:
                    d = datetime.datetime.strptime(dt, f)
                    return int(1000 * (time.mktime(d.timetuple()) + d.microsecond * 1e-6))
                except ValueError:
                    continue
                # get response function

    def get_response(self, res, clz):
        """ Read the response and return it as an object of its class."""
        parts = clz.split(".")
        module = ".".join(parts[:2])
        m = __import__(module)
        for comp in parts[2:]:
            m = getattr(m, comp)
            o = m()
            o.parsedata(parsejson(res))
            return o

    # get error function
    def get_errorinfo(self, statuscode, jsonres):
        """ Return error object"""
        info = errorinfo()
        info.set_httpstatus(statuscode)
        return self.get_response(jsonres, "iotticket.models.errorinfo")

    # get device function
    def getdevice(self, deviceId):
        """Function to get information of a device"""
        pathUrl = self.baseUrl + self.specificdeviceresourceformat.format(deviceId)
        return self.connect(pathUrl, "iotticket.models.device")

    # get devices function
    def getdevices(self, limit=10, offset=0):
        """Function to get list of devices."""
        if (limit > 100):
            limit = 100
        param = "?limit=" + str(limit) + "&offset=" + str(offset)
        pathUrl = self.baseUrl + self.deviceresource + param
        return self.connect(pathUrl, "iotticket.models.devices")

    # get datanode list function
    def getdatanodeslist(self, deviceId, limit=10, offset=0):
        """Function to get datanode list"""
        if (limit > 100):
            limit = 100
        param = "?limit=" + str(limit) + "&offset=" + str(offset)
        pathUrl = self.baseUrl + self.datanodesresourceformat.format(deviceId) + param
        return self.connect(pathUrl, "iotticket.models.datanodes")

    # get all quota function
    def getallquota(self):
        """Function to get all quota."""
        pathUrl = self.baseUrl + self.quotaallresource
        return self.connect(pathUrl, "iotticket.models.quota")

    # get device quota function
    def getdevicequota(self, deviceId):
        """Function to get quota of a device."""
        pathUrl = self.baseUrl + self.quotadeviceresourceformat.format(deviceId)
        return self.connect(pathUrl, "iotticket.models.devicequota")

    # move device function
    def movedevice(self,deviceid,enterpriseid):
        try:
            destination={"enterpriseId":enterpriseid}
            j=json.dumps(destination)
            data=j.encode("utf8")
            pathUrl=self.baseUrl+self.deviceresource+"move/"+deviceid+"/"
            req = urllib.request.Request(pathUrl, data=data, headers=self.headers)
            with urllib.request.urlopen(req, context=self.context) as response:
                response = response.read()

        except err.HTTPError as e:
            raise self.get_errorinfo(e.code, e.read()) from None
        else:
            return self.get_response(response, "iotticket.models.device")

    # register device function
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

    # read data function
    def readdata(self, deviceId, criteriaobj, fromdater=None, todater=None, limit=1000, order="ascending"):
        """Function to read datanode value."""
        if (limit > 10000):
            limit = 10000
        critlist = ""
        pr = ""
        for cr in criteriaobj.criterialist:
            if (criteriaobj.criterialist.index(cr) != len(criteriaobj.criterialist) - 1):
                critlist += cr + ","
            else:
                critlist += cr
        critlist = critlist.replace(" ", "%20")
        fromdate = self.dttots(fromdater)
        todate = self.dttots(todater)
        if fromdate == None:
            fromdate = 0
        if todate == None:
            todate = 0
        if (fromdate == 0 and todate > 0):
            fromdate = 0
            todate = 0
        if (fromdate > 0):
            pr += "&fromdate=" + str(fromdate)
        if (todate > 0):
            pr += "&todate=" + str(todate)
        if (limit != 1000):
            pr += "&limit=" + str(limit)
        if (order == "ascending" or order == "descending"):
            pr += "&order=" + order
        param = "?datanodes=" + critlist + pr
        pathUrl = self.baseUrl + self.readdataresourceformat.format(deviceId) + param
        return self.connect(pathUrl, "iotticket.models.datanodesvaluelist")

    # write data node function
    def writedata(self, deviceId, *datanodevalueobj):
        """Function to write data to server."""
        dv = []
        for dvo in datanodevalueobj:
            if (validate(dvo)):
                dv.append(dvo.__dict__)
        if len(dv) > 0:
            try:
                j = json.dumps(dv)
                data = j.encode("utf8")
                pathUrl = self.baseUrl + self.writedataresourceformat.format(deviceId)

                req = urllib.request.Request(pathUrl, data=data, headers=self.headers)

                with urllib.request.urlopen(req, context=self.context) as response:
                    response = response.read()
            except err.HTTPError as e:
                raise self.get_errorinfo(e.code, e.read()) from None
            else:
                return self.get_response(response, "iotticket.models.writeresults")
        else:
            return "All datanodes are not valid"