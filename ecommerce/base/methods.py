SUCCESS = True
FAIL = False

def getPositiveResponse(msg, status_code=200, data={}):
    response = {}
    response['status'] = SUCCESS
    response['message'] = msg
    response['statusCode'] = status_code
    response['result'] = data
    return response

def getNegativeResponse(msg, status_code=400, result={}):
    response = {}
    response['status'] = FAIL
    response['message'] = msg
    response['statusCode'] = status_code
    response['result'] = result
    return response