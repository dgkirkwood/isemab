"""
access
YTgzMzQ1ZGUtNzQ5Yy00MjY2LThlYmItM2JlZjM4ZjM3YzkzZTk4ZDk2ZTUtYjEy



room
Y2lzY29zcGFyazovL3VzL1JPT00vNWU4ZGEwMzItMTc3Ni0zODhmLTg4YWItODRkZmNkZGVjYWVl
"""

#my actor ID Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNmE0ODJhNy00NjEzLTRiN2MtYWYxZi1kMzI2ZDZhNzQyZGQ
#bot actor ID Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zN2E0MmY3NS05YzBkLTQxMjMtYjgyMS01MDY0NjQyZTg0NTc



from flask import Flask, request, session, redirect 
import json
from ISEAPI import SparkAPI
from ISEAPI import ISEAPI
import re
import io
import os

server = "198.19.10.27"
username = "ERSAdmin"
password = "C1sco12345"

roomID = "Y2lzY29zcGFyazovL3VzL1JPT00vNWU4ZGEwMzItMTc3Ni0zODhmLTg4YWItODRkZmNkZGVjYWVl"
botToken = "YTgzMzQ1ZGUtNzQ5Yy00MjY2LThlYmItM2JlZjM4ZjM3YzkzZTk4ZDk2ZTUtYjEy"
botID = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zN2E0MmY3NS05YzBkLTQxMjMtYjgyMS01MDY0NjQyZTg0NTc"

ISEReq = ISEAPI(server, username, password)
maccheck = re.compile('^([0-9A-Fa-f]{2}[:.-]){5}([0-9A-Fa-f]{2})$')


def oldMacCheck(macAddress):
	oldMac = macAddress
	if maccheck.match(oldMac):
		transMac = ISEReq.MacTransform(oldMac)

		print transMac
		root = ISEReq.GetAllEndpoints()
		#print root
		deviceFound = False
		deviceDict = {}
		for resources in root:
			for resource in resources:
				a =resource.attrib
				deviceDict[a['name']] = a['id']
				"""
				if ((a['name'])==(transMac)):
					print "MATCH!!"
					
					deviceID = a['id']
					#print deviceID
					deviceFound = True					
					oldDeviceInfo = ISEReq.GetEndpointByID(deviceID)
				"""
					
		
		#print deviceDict
		print "The transMac is "+transMac
		if transMac in deviceDict:
			deviceID = deviceDict[transMac]
			oldDeviceInfo = ISEReq.GetEndpointByID(deviceID)	
			return oldDeviceInfo
		else:
			return 'NOTFOUND'
				

	else:
		return 'NOTMAC'

def newMacCreate(macAddress, oldDeviceID, oldGroupID, oldProfileID):
	newmac = macAddress
	if maccheck.match(newmac):
		newmac = ISEReq.MacTransform(newmac)

		newDeviceInfo = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<ns4:endpoint description=\"description\" id=\"id\" name=\"name\" xmlns:ers=\"ers.ise.cisco.com\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:ns4=\"identity.ers.ise.cisco.com\">\n    <groupId>"+str(oldGroupID)+"</groupId>\n    <identityStore></identityStore>\n    <identityStoreId></identityStoreId>\n    <mac>"+newmac+"</mac>\n    <portalUser></portalUser>\n    <profileId>"+str(oldProfileID)+"</profileId>\n    <staticGroupAssignment>true</staticGroupAssignment>\n    <staticProfileAssignment>true</staticProfileAssignment>\n</ns4:endpoint>"

		doCreate = ISEReq.CreateEndpoint(newDeviceInfo)

		if doCreate == True:

			return ISEReq.DeleteEndpoint(oldDeviceID)




	else:
		return 'NOTMAC'


app = Flask(__name__)

@app.route('/',methods=['POST'])
def listener():
	data = json.loads(request.data)
	messageID = data['data']['id']

	if data['actorId'] != botID:
		sparkCall = SparkAPI(roomID, botToken)
		message = sparkCall.GETMessage(messageID)

		prettymessage = json.loads(message)
		
		if prettymessage["text"][0] in ("O", "o"):
			
			macOnly = (prettymessage["text"][4:21])
			
			check = oldMacCheck(macOnly)


			if check == 'NOTMAC':
				
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \""+macOnly+" does not appear to be a valid MAC address. Please ensure you enter 12 hexadecimal characters in pairs separated by ':'' , '.'' or '-'. For example aa:bb:cc:11:22:33\"\n}"

				sparkCall.POSTMessage(payload)

			elif check == 'NOTFOUND':
				
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"The MAC address "+macOnly+" was not found in the ISE database. Please check the address again or contact your IT department.\"\n}"

				sparkCall.POSTMessage(payload)

			else:

				data = check
				with io.open('data.json', 'w', encoding='utf8') as outfile:
					str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
					outfile.write(str_)				
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"Device found. Please enter the MAC address of the new device being installed.\"\n}"
				sparkCall.POSTMessage(payload)


				return "OK"


		elif prettymessage["text"][0] in ("N", "n"):
			

			macOnly = (prettymessage["text"][4:21])

			if os.path.isfile('data.json') == True:

				with open('data.json') as data_file:
					data_loaded = json.load(data_file)

			else:
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"You have not yet entered data on the device you would like to replace. Identify the old device using \'old AA:BB:CC:11:22:33\'\"\n}"

				sparkCall.POSTMessage(payload)

				return "OK"					

			oldDeviceID = data_loaded["ns4:endpoint"]["@id"]
			oldGroupID = data_loaded["ns4:endpoint"]["groupId"]
			oldProfileID = data_loaded["ns4:endpoint"]["profileId"]

			creator = newMacCreate(macOnly, oldDeviceID, oldGroupID, oldProfileID)

			if creator == True:
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"Device with mac "+macOnly+" is now authorised to access the network.\"\n}"
				sparkCall.POSTMessage(payload)
				os.remove('data.json')				
				return "OK"
			elif creator == 'NOTMAC':
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \""+macOnly+" does not appear to be a valid MAC address. Please ensure you enter 12 hexadecimal characters in pairs separated by ':'' , '.'' or '-'. For example aa:bb:cc:11:22:33\"\n}"

				sparkCall.POSTMessage(payload)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

