from flask import jsonify, abort

def response_with(body):
    try:
        response = jsonify(body)
        response.status ='400' if 'errCode' in body else '200'
        return response
    except Exception as ex:
        abort(400)