import urllib2
import urllib
import sqlite3
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
endpointUrl = raw_input("\033[94mPlease type endpoint URL where Dilbert should POST the data:\033[0m ")

#=============================
# WHILE LOOP
#=============================
dilbertEndpointUrl = dilberthost + responseGuid.read().replace('"', "")
req = urllib2.Request(dilbertEndpointUrl)
req2 = urllib2.Request(endpointUrl)
while True:
	fakeData = urllib2.urlopen(req)
	print fakeData.read()
	sleep(interval)

#=============================
# STORING INTO LOCAL DB
#=============================
# conn = sqlite3.connect('mocks.db')
# c = conn.cursor()

# c.execute("INSERT INTO sensors VALUES (" + serviceType + ", 5)")

# conn.commit()
# conn.close()