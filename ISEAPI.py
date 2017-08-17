import requests
from lxml import etree
import xmltodict


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ISEAPI(object):

	def __init__(self, server, username, password):
		self.server = server
		self.username = username
		self.password = password


	def ISEGET(self, url, headers):

		try:
			response = requests.request("GET", url, auth=(self.username,self.password), headers=headers, verify=False)
			status_code = response.status_code
			if (status_code == 200):
				root = etree.fromstring(str(response.text))
				return root
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()


	def ISEGET2(self, url, headers):

		try:
			response = requests.request("GET", url, auth=(self.username,self.password), headers=headers, verify=False)
			status_code = response.status_code
			if (status_code == 200):
				root = xmltodict.parse(response.text)
				return root
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()


	def ISEPOST(self, url, headers, content):

		try:
			response = requests.request("POST", url, auth=(self.username,self.password), headers=headers, data=content, verify=False)
			status_code = response.status_code
			if (status_code == 201):
				return True
			else:
				response.raise_for_status()
				print("Error occured in POST -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()


	def ISEDELETE(self, url, headers):

		try:
			response = requests.request("DELETE", url, auth=(self.username,self.password), headers=headers, verify=False)
			status_code = response.status_code
			if (status_code == 204):
				return True
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()


	def GetAllEndpoints(self):
		"""
		XXXXX
		"""
		myurl = "https://"+self.server+":9060/ers/config/endpoint"
		headers = {'accept': "application/vnd.com.cisco.ise.identity.endpoint.1.0+xml"}
		return self.ISEGET(myurl, headers)
		


	def GetEndpointByID(self, endpointID):
		"""
		XXXXXX
		"""
		myurl = "https://"+self.server+":9060/ers/config/endpoint/"+endpointID
		headers = {'accept' : "application/vnd.com.cisco.ise.identity.endpoint.1.0+xml;"}
		return self.ISEGET2(myurl, headers)


	def CreateEndpoint(self, content):
		"""
		XXXXX
		"""
		myurl = "https://"+self.server+":9060/ers/config/endpoint"
		headers = {'content-type': "application/vnd.com.cisco.ise.identity.endpoint.1.0+xml; charset=utf-8"}
		#print content
		return self.ISEPOST(myurl, headers, content)


	def DeleteEndpoint(self, endpointID):
		"""
		XXXXX
		"""
		myurl = "https://"+self.server+":9060/ers/config/endpoint/"+endpointID
		headers = {'accept': "application/vnd.com.cisco.ise.identity.endpoint.1.0+xml"}
		return self.ISEDELETE(myurl, headers)


	def MacTransform(self, macAddress):
		"""
		XXX
		"""
		letters = (":" if i % 3 == 0 else char for i, char in enumerate(macAddress.upper(), 1))
		transMac = str(''.join(letters))
		return transMac



class SparkAPI(object):

	def __init__(self, roomID, botID):
		self.roomID = roomID
		self.botID = botID

	def SparkGET(self, url, headers):
		
		try:
			response = requests.request("GET", url, headers=headers, verify=False)
			status_code = response.status_code
			if (status_code == 200):
				return response.text
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()


	def SparkPOST(self, url, headers, payload):
		
		try:
			response = requests.request("POST", url, headers=headers, data=payload, verify=False)
			status_code = response.status_code
			if (status_code == 200):
				return response.text
			else:
				response.raise_for_status()
				print("Error occured in GET -->"+(response.text))
		except requests.exceptions.HTTPError as err:
			print ("Error in connection -->"+str(err))
		finally:
			if response : response.close()



	def GETMessage(self, messageID):
		
		url = 'https://api.ciscospark.com/v1/messages/'+messageID
		headers = {'content-type' : 'application/json; charset=utf-8', 'authorization' : "Bearer "+self.botID}
		return self.SparkGET(url, headers)

	def POSTMessage(self, payload):

		url = 'https://api.ciscospark.com/v1/messages'
		headers = {'content-type' : 'application/json; charset=utf-8', 'authorization' : "Bearer "+self.botID}
		return self.SparkPOST(url, headers, payload)


