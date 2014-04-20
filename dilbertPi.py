import urllib2
import urllib
import json
from time import sleep

dilberthost = 'http://localhost:1337/'

print "\033[94mWhat type of sensor would you like to mock?\033[0m"
print "1) iBeacon (Presence)"
print "2) Temperature"
print "3) Proximity"

input = int(raw_input("Choose your option: "))

#=============================
# CREATING DILBERT ENDPOINT
#=============================
if input == 1:
	serviceType = 'ibeacon'
elif input == 2 :
	serviceType = 'temperature'
elif input == 3:
	serviceType = 'proximity'

values = {
		  'httpStatus' : '200',
          'type' : 'singlevalue',
          'data[0][valueType]' : serviceType
         }

headers = { 'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8' }
data = urllib.urlencode(values)

req = urllib2.Request(dilberthost + 'endpoint/create', data, headers)
responseGuid = urllib2.urlopen(req)

#=============================
# ASKING FOR INTERVAL
#=============================
interval = float(raw_input("\033[94mHow frequent (in seconds) do you want me to sense?:\033[0m "))

#=============================
# ASKING FOR ENDPOINT
#=============================
endpointUrl = raw_input("\033[94mType endpoint URL where Dilbert should POST the data:\033[0m ")

#=============================
# WHILE LOOP
#=============================
dilbertEndpointUrl = dilberthost + responseGuid.read().replace('"', "")
dilbertRequest = urllib2.Request(dilbertEndpointUrl)
count = 1
while True:
	
	# GETTING FAKE DATA FROM DILBERT
	fakeDataResponse = urllib2.urlopen(dilbertRequest)
	fakeData = fakeDataResponse.read()
	fakeDataJson = json.loads(fakeData)

	# POSTING THE FAKE DATA TO THE USER-DEFINED ENDPOINT
	data = urllib.urlencode(fakeDataJson)
	headers = { 'Content-type' : 'application/json' }
	endpointRequest = urllib2.Request(endpointUrl, data, headers)
	urllib2.urlopen(endpointRequest)
	
	# data = urllib.urlencode(fakeDataJson)
	# headers = { 'Content-type' : 'application/json' }
	# endpointRequest = urllib2.Request(endpointUrl, data, headers)
	# try: 
	# 	urllib2.urlopen(endpointRequest)
	# except urllib2.HTTPError, e:
	# 	print "HTTPError = " + str(e.code)
	# except urllib2.URLError, e:
	#     print "URLError = " + str(e.reason)

	sleep(interval)
	count = count + 1
