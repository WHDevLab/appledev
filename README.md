App Store Connect Api
====

This is a Python wrapper around the **Apple App Store Api** : https://developer.apple.com/documentation/appstoreconnectapi

So far, it handles token generation / expiration, methods for listing resources and downloading reports. 

Installation
------------

The project is published on PyPI, install with: 

    pip install appstoreconnectapi

Usage
-----

Please follow instructions on [Apple documentation](https://developer.apple.com/documentation/appstoreconnectapi/creating_api_keys_for_app_store_connect_api) on how to generate an API key.

With your *key ID*, *key file* and *issuer ID* create a new API instance:

```python
from appstoreconnectapi import AppStoreConnect
asc = AppStoreConnect(key_id, path_to_key_file, issuer_id)
```

Here are a few examples of API usage

```python
# list all profiles
profiles = asc.getProfiles()
print profiles

#list all certificates
certificates = asc.getCertificates()
print profiles

#download profile
asc.downloadProfile(profileID='xxxxx', saveFolderPath='./'):

#download certificate
asc.downloadCertificate(certificatID='xxxxx', saveFolderPath='./'):

#other api，for example list all bundleids
#method: get or post
res = asc.fetch(uri='/v1/bundleIds', method='get', post_data=None)
print res

```

more api goto https://developer.apple.com/documentation/appstoreconnectapi
