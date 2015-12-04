#! /usr/bin/env python

# A visulization project of IoT 2015, Thayer School, Dartmouth
# Developer: Yuchen Su
# Team members: Jinke Li, Xinyue Zheng
# Date: 12/04/2015
# Version 0.01

# Please Use your own api keys for google and twitter api's

import time, requests, urllib, sys
import RPi.GPIO as GPIO
from requests_oauthlib import OAuth1


api_key2 = {'ck':'Consumer Key','cs':'Consumer Seceret','at':'Access Token','ats':'Access Token Secret'}

def fetchTwitterLocation(queryContent):

	"""
	Use Twitter Api to get 20 tweets at one time;
	This function returns a list of locations of these 20 tweets;
	It filters out tweets that do not have location information
	"""

        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        query = {'q': queryContent, 'count': 200}
        url = url + urllib.urlencode(query)
        auth = OAuth1(api_key2['ck'],api_key2['cs'],api_key2['at'],api_key2['ats'])
        r = requests.get(url,auth=auth)
        t = r.json()
	loc = ''   # default value
	locList = []
	for tweet in t['statuses']:
		try:
			loc =  tweet['user']['location']
			if loc.strip() == '':
				continue
			else:
				locList.append(loc)
		except KeyError:
			pass
	return reversed(locList)

def setup(pinList):

	"""
	This function setups the mode of raspberry pi
	"""

	GPIO.setmode(GPIO.BCM)
	for pin in pinList:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,1)


def dtob(n):

	"""
	Transforms a decimal number to a binary number.
	Puts zeros in the front of the number in case it does not have 10 digits
	"""
	nd = bin(n)[2:]
	return ''.join([(10 - len(nd))*'0',nd])

def ligthUpLed(pinList,bincode):

	"""
	Lights up leds
	0V to light up
	"""
	for c in xrange(len(bincode)):
		GPIO.output(pinList[c],1-int(bincode[c]))

def clearUp(pinList):

	"""
	Put out all leds when KeyInterrupt happens
	"""
	for i in pinList:
		GPIO.output(i,1)

def buildUrl(org,dis,key):

	"""
	Use google api to get the driving distance between one place to another
	Places that cannot be driven to will raise key error; Use exception to catch this error
	"""
	udict = {'origins':org, 'destinations':dis, 'key':key}
	return 'https://maps.googleapis.com/maps/api/distancematrix/json?'+urllib.urlencode(udict)

def getRequestJson(url):
	r = requests.get(url)
	return r.json()

def main():
	pinList = [17,27,22,5,6,13,19,26,21,20]
	api_key = 'Google Api Key'
	setup(pinList)
	try:
		while True:
			locList = fetchTwitterLocation(sys.argv[1])
			for org in locList:
				print org
				dist = 'Hanover NH'
				try:
					url = buildUrl(org,dist,api_key)
				except UnicodeEncodeError:
					print "[-] UnicodeEncodeError happened"
					continue
				jt = getRequestJson(url)
				try:
					dt = jt['rows'][0]['elements'][0]['distance']['text']
				except KeyError:
					print "[-] Distance KeyError happened"
					continue
				print '[+]'+ dt
				clearUp(pinList)
				time.sleep(0.5)
				ligthUpLed(pinList,dtob(int(''.join(dt[:-3].split(',')))/10))
				time.sleep(4)
			time.sleep(10)
	except KeyboardInterrupt:
		clearUp(pinList)

if __name__ == "__main__":
	main()
