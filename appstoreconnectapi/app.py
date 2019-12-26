import requests
import jwt
import gzip
from datetime import datetime, timedelta
import time
import json
import base64

ALGORITHM = 'ES256'
BASE_API = "https://api.appstoreconnect.apple.com"


class AppStoreConnect:
	def __init__(self, key_id, key_file, issuer_id):
		self._token = None
		self.token_gen_date = None
		self.exp = None
		self.key_id = key_id
		self.key_file = key_file
		self.issuer_id = issuer_id
		self._debug = False
		token = self.token  # generate first token

	@property
	def token(self):
		# generate a new token every 15 minutes
		if not self._token or self.token_gen_date + timedelta(minutes=15) < datetime.now():
			self._token = self._generate_token()

		return self._token

	def _generate_token(self):
		key = open(self.key_file, 'r').read()
		self.token_gen_date = datetime.now()
		exp = int(time.mktime((self.token_gen_date + timedelta(minutes=20)).timetuple()))
		return jwt.encode({'iss': self.issuer_id, 'exp': exp, 'aud': 'appstoreconnect-v1'}, key,
		                   headers={'kid': self.key_id, 'typ': 'JWT'}, algorithm=ALGORITHM).decode('ascii')

			
	def _api_call(self, uri, method="get", post_data=None):
		headers = {"Authorization": "Bearer %s" % self.token}
		if self._debug:
			print(uri)
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
			# TODO implement stream decompress
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

