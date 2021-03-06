import urllib2
import urllib
import json
from time import sleep

dilberthost = 'http://geekster.io:8080/'
#dilberthost = 'http://localhost:1337/'

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
# ASKING FOR INTERVAL & ENDPOINT
#=============================
interval = float(raw_input("\033[94mHow frequent (in seconds) do you want Dilbert to sense?:\033[0m "))
print "\033[92mPlease select an output format\033[0m"
print "1) POST to an Endpoint"
print "2) Print in console"
print "3) Save locally into Json file"
outputFormat = int(raw_input("\033[92mChoose your option: \033[0m "))

if outputFormat == 1:
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

	# FEEDBACK IN TERMINAL
	if count % 2 == 0:
		print "\033[92m"
	else:
		print "\033[93m"
	print fakeData

	# POSTING THE FAKE DATA TO THE USER-DEFINED ENDPOINT
	if outputFormat == 1:

		endpointRequest = urllib2.Request(endpointUrl, fakeData, { 'Content-type' : 'application/json' })
		print "Sending POST to " + endpointUrl

		try: 
			urllib2.urlopen(endpointRequest)
		except urllib2.HTTPError, e:
			print "HTTPError = " + str(e.code)
		except urllib2.URLError, e:
		    print "URLError = " + str(e.reason)

		sleep(interval)
		count = count + 1

	print "\033[0m"