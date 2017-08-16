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

server = "198.19.10.27"
username = "ERSAdmin"
password = "C1sco12345"

roomID = "Y2lzY29zcGFyazovL3VzL1JPT00vNWU4ZGEwMzItMTc3Ni0zODhmLTg4YWItODRkZmNkZGVjYWVl"
botToken = "YTgzMzQ1ZGUtNzQ5Yy00MjY2LThlYmItM2JlZjM4ZjM3YzkzZTk4ZDk2ZTUtYjEy"
botID = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zN2E0MmY3NS05YzBkLTQxMjMtYjgyMS01MDY0NjQyZTg0NTc"

ISEReq = ISEAPI(server, username, password)
maccheck = re.compile('^([0-9A-Fa-f]{2}[:.-]){5}([0-9A-Fa-f]{2})$')


def oldMacCheck(macAddress):
	oldmac = macAddress
	if maccheck.match(oldmac):
		oldmac = ISEReq.MacTransform(oldmac)
		root = ISEReq.GetAllEndpoints()
		print root

		for resources in root:
			for resource in resources:
				a =resource.attrib
				if ((a['name'])==(oldmac)):
					deviceID = a['id']
					oldDeviceInfo = ISEReq.GetEndpointByID(deviceID)
					return oldDeviceInfo
				else:
					return 'NOTFOUND'

	else:
		return 'NOTMAC'

def newMacCreate(macAddress, oldDeviceID):
	newmac = macAddress
	if maccheck.match(newmac):
		newmac = ISEReq.MacTransform(newmac)

		newDeviceInfo = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<ns4:endpoint description=\"description\" id=\"id\" name=\"name\" xmlns:ers=\"ers.ise.cisco.com\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:ns4=\"identity.ers.ise.cisco.com\">\n    <groupId>"+str(oldDeviceInfo["ns4:endpoint"]["groupId"])+"</groupId>\n    <identityStore></identityStore>\n    <identityStoreId></identityStoreId>\n    <mac>"+newmac+"</mac>\n    <portalUser></portalUser>\n    <profileId>"+str(oldDeviceInfo["ns4:endpoint"]["profileId"])+"</profileId>\n    <staticGroupAssignment>true</staticGroupAssignment>\n    <staticProfileAssignment>true</staticProfileAssignment>\n</ns4:endpoint>"

		doCreate = ISEReq.CreateEndpoint(newDeviceInfo)

		if doCreate == True:
			ISEReq.DeleteEndpoint(oldDeviceID)


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
				
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"Please ensure you enter 12 hexadecimal characters in pairs separated by ':'' , '.'' or '-'. For example aa:bb:cc:11:22:33.\"\n}"
				#print payload
				sparkCall.POSTMessage(payload)

			elif check == 'NOTFOUND':
				

				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"The MAC address "+macOnly+" was not found in the ISE database. Please check the address again or contact your IT department.\"\n}"
				print payload
				sparkCall.POSTMessage(payload)

			else:
				
				print check
				data = check
				with io.open('data.json', 'w', encoding='utf8') as outfile:
					str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
					outfile.write(str_)				
				payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"Device found. Please enter the MAC address of the new device being installed.\"\n}"
				sparkCall.POSTMessage(payload)				


			return "OK"


		elif prettymessage["text"][0] in ("N", "n"):
			print "RAWR"

			#macOnly = (prettymessage["text"][4:21])



			return "OK"
			
"""

@app.route('/checkOldMac', methods=['POST'])
def checkOldMac():
	data = json.loads(request.data)
	messageID = data['data']['id']
	print messageID
	return "OK"

	#print prettymessage["text"]


	check = oldMacCheck(prettymessage["text"])
	
	if check == 'NOTMAC':
		
		payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"Please ensure you enter 12 hexadecimal characters in pairs separated by ':'' , '.'' or '-'. For example aa:bb:cc:11:22:33.\"\n}"
		#print payload
		sparkCall.POSTMessage(payload)

	elif check == 'NOTFOUND':
		

		payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"The MAC address "+prettymessage["text"]+" was not found in ISE database. Please check the address again or contact your IT department.\"\n}"
		print payload
		sparkCall.POSTMessage(payload)

	else:
		
		payload = "{\n  \"roomId\" : \""+roomID+"\",\n  \"text\" : \"Device found. Please enter the MAC address of the new device being installed.\"\n}"
		sparkCall.POSTMessage(payload)





"""



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)




