import requests
import jwt
import gzip
from datetime import datetime, timedelta
import time
import json
import base64

class Auth:
	def __init__(self, key_id, key_file, issuer_id):
		self.token = None
		self.token_gen_date = None
		self.exp = None
		self.key_id = key_id
		self.key_file = key_file
		self.issuer_id = issuer_id
	
	def get_token(self):
		# generate a new token every 15 minutes
		if not self.token or self.token_gen_date + timedelta(minutes=15) < datetime.now():
			self.token = self.generate_token()

		return self.token

	def generate_token(self):
		key = open(self.key_file, 'r').read()
		self.token_gen_date = datetime.now()
		exp = int(time.mktime((self.token_gen_date + timedelta(minutes=20)).timetuple()))
		return jwt.encode({'iss': self.issuer_id, 'exp': exp, 'aud': 'appstoreconnect-v1'}, key,
							headers={'kid': self.key_id, 'typ': 'JWT'}, algorithm='ES256')