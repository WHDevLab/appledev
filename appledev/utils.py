import json
def dump_response(response):
	if type(response) == dict:
		return response
	rJson = json.loads(response.text)
	return rJson

def isSuccess(jsonData):
	if 'errors' in jsonData:
		return False
	return True
# def appleResponseHandle(jsondata):
# 	if 'errors' in jsondata:
# 		errors = jsondata["errors"]
# 		if len(errors) > 0:
# 			error = errors[0]
# 			return res_json(error["status"], msg=error["detail"])

# 	return res_json(200)

