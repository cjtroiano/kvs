from flask import Flask
from flask import request
from flask import jsonify
#from flask_restful import Resource, Api
app = Flask(__name__)
#api = Api(app)

kvs = {}

@app.route('/hello')
def hello_world():
	#if request.method == 'POST':
	#	app.error_handler_spec[None][405] = METHOD_NOT_ALLOWED
	return 'Hello World!'


@app.route('/echo')
def echobot():
		msg = request.args.get('msg')
		if msg is None:
			return ""
		else:
			return msg



@app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])
def initKVS(key):

	# x = VALUE
	x = request.form.get('val')


	#Do PUT
	if request.method == 'PUT':
		#insert new key value into dict
		if kvs.get(key) == None:
			kvs[key] = x
			data = {
			'replaced' : 0,
			'msg' : 'success'
			}
			response = jsonify(data)
			response.status_code = 201
			return response

		#replace value of key with new value	
		else:
			kvs[key] =x
			data = {
			'replaced' : 1,
			'msg' : 'success'
			}
			response = jsonify(data)
			response.status_code = 200
			return response

	#Do DELETE
	if request.method == 'DELETE':
		if kvs.get(key) == None:
			data = {
			'msg' : 'error',
			'error' : 'key does not exist'
			}
			response = jsonify(data)
			response.status_code = 404
			return response
		else:
			del kvs[key]
			data = {
			'msg' : 'success'
			}
			response = jsonify(data)
			response.status_code = 200
			return response

	#Do GET		
	else:
		#key value does not exist 
		if kvs.get(key) == None:
			data = {
			'msg' : 'error',
			'error' : 'key does not exist'
			}
			response = jsonify(data)
			response.status_code = 404
			return response
		#key value does exist
		else:
			x = kvs.get(key)
			data = {
			'msg' : 'success',
			'value' : x
			}
			response = jsonify(data)
			response.status_code = 404
			return response	

#def checkT(key, value):


if __name__ == '__main__':
	#x = 'asd'
	#f = hash(x, 10)
	#print f
	app.debug = True
	app.run(host='0.0.0.0',port=8080)