import requests
import jwt
import gzip
from datetime import datetime, timedelta
import time
import json
import base64
from auth import Auth
import utils
BASE_API = "https://api.appstoreconnect.apple.com"


class AppStoreConnect:
	def __init__(self, key_id, key_file, issuer_id):
		self.auth = Auth(key_id, key_file, issuer_id)
			
	def _api_call(self, uri, method="get", post_data=None):
		headers = {"Authorization": "Bearer %s" % self.auth.get_token()}
		r = {}

		url = BASE_API+uri
		if method.lower() == "get":
			r = requests.get(url, headers=headers)
		elif method.lower() == "post":
			headers["Content-Type"] = "application/json"
			r = requests.post(url=url, headers=headers, data=json.dumps(post_data))
		elif method.lower() == "patch":
			headers["Content-Type"] = "application/json"
			r = requests.patch(url=url, headers=headers, data=json.dumps(post_data))

		content_type = r.headers['content-type']

		if content_type == "application/json":
			payload = r.json()
			return payload
		elif content_type == 'application/a-gzip':
			data_gz = b""
			for chunk in r.iter_content(1024 * 1024):
				if chunk:
					data_gz = data_gz + chunk

			data = gzip.decompress(data_gz)
			return data.decode("utf-8")
		else:
			return r
		

	def fetch(self, uri, method="get", post_data=None):
		return self._api_call(uri, method, post_data)
		
	def registerDevice(self, name, udid):
		attributes = {"udid":udid, "name":name, "platform":"IOS"}
		data = {"data":{"type":"devices", "attributes":attributes}}
		response = self.fetch(uri="/v1/devices", method="post", post_data=data)
		jsondata = utils.dump_response(response)
		errors = jsondata["errors"]
		if len(errors) == 0:
			print("操作成功")
		return jsondata

	def getDevices(self):
		response = self.fetch(uri="/v1/devices")
		jsondata = utils.dump_response(response)
		return jsondata

	# IOS_APP_DEVELOPMENT, IOS_APP_STORE, IOS_APP_ADHOC, IOS_APP_INHOUSE, MAC_APP_DEVELOPMENT, MAC_APP_STORE, MAC_APP_DIRECT, TVOS_APP_DEVELOPMENT, TVOS_APP_STORE, TVOS_APP_ADHOC, TVOS_APP_INHOUSE, MAC_CATALYST_APP_DEVELOPMENT, MAC_CATALYST_APP_STORE, MAC_CATALYST_APP_DIRECT
	def createProfile(self, name, bid, cids, devices):
		attributes = {"name":name, "profileType":"IOS_APP_ADHOC"}
		bundleId = {"id":bid,"type":"bundleIds"}
		certificates = []
		for cid in cids:
			certificates.append({"id":cid, "type":"certificates"})
		
		devices = []
		for did in devices:
			devices.append({"id":did, "type":"devices"})

		relationships = {"bundleId":{"data":bundleId}, "certificates":{"data":certificates}, "devices":{"data":devices}}
		data = {"data":{"type":"profiles", "attributes":attributes, "relationships":relationships}}
		response = self.fetch(uri="/v1/bundleIds", method="post", post_data=data)
		jsondata = utils.dump_response(response)
		return jsondata

	def getProfiles(self):
		return self._api_call("/v1/profiles")

	def downloadProfile(self, profileID=None, saveFolderPath=None):
		try:
			r = self._api_call("/v1/profiles/"+profileID)
			r = r.json()
			attributes = r["data"]["attributes"]
			profileContent = attributes["profileContent"]
			name = attributes["uuid"]
			saveFilePath = saveFolderPath+"/"+name+".mobileprovision"
			f = open(saveFilePath, "w")
			f.write(base64.b64decode(profileContent))
			f.close()
			return "success"
		except FileNotFoundError:
			return "failure"

	def getCertificates(self):
		return self._api_call("/v1/certificates")


	def downloadCertificate(self, certificatID=None, saveFolderPath=None):
		try:
			r = self._api_call("/v1/certificates/"+certificatID)
			r = r.json()
			attributes = r["data"]["attributes"]
			certificateContent = attributes["certificateContent"]
			name = attributes["name"]
			saveFilePath = name+".cer"
			f = open(saveFilePath, "w")
			f.write(base64.b64decode(certificateContent))
			f.close()
			return "success"
		except FileNotFoundError:
			return "failure"
