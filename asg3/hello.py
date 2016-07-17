import requests
import json
#import jsonify
import os
import sys
from flask import Flask, Response
from flask import request
from flask import jsonify
#from flask import session

#from flask_restful import Resource, Api
app = Flask(__name__)
#api = Api(app)


#The key value store
kvs = {}
ip = os.environ['IP']
port = os.environ['PORT']
members = os.environ['MEMBERS']

#Initialize the first list of nodes =! primary node
membersk=str(members)
memberslist=membersk.split(',')
memberslistIds =[x[8:9] for x in memberslist]

#This is the default master/primary node
masternode=min(memberslistIds)
memberslistIds.remove(masternode)


@app.route('/myip')
def whatip():
	x = request.remote_addr
	return x + '\n'
	#return jsonify({'ip': request.remote_addr}), 200su

@app.route('/myport')
def whatport():
	x = request.host
	return x

@app.route('/masters')
def master():
 	return memberslist[1]

@app.route('/check')
def check():
	a = int(masternode)
	b = a + 5
	c = str(b)
	return c

#TEST PARSING JSON RESPONSES FROM A NODE
@app.route('/cget')
def checkmasterx():
	r = requests.get('http://10.0.0.21:12346/kvs/foo')
	data=r.json()
	#x = data['key']
	return str(data['value'])

#CHECK IF THE IP ADDRESS IS FROM A NODE OR USER
@app.route('/test')
def node():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[0]
	if ipnum == 'localhost':
		return 0
	else:
		return 1
	#ipnode = ipnum[4:5]
	#return ipnode

#TEST SENDING AND RECEIVING MASTER NODE DATA
@app.route('/cmon')
def checkmaster():
	r = requests.get('http://10.0.0.20:12345/kk')
	x = nodek()
	return str(r.text) + '\n' + masternode + '\n' + x + '\n'

#RETURN NODE ID
@app.route('/kk')
def nodek():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[0]
	ipnode = ipnum[8:9]
	return ipnode	

#CHECK IF THE IP ADDRESS IS FROM A NODE / SAME AS node()
def isnode():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[0]
	if ipnum[7:8] == '2':
		return True 
	else:
		return False

#Check if client requests goes to masternode.
def isMasterUser():
	node = whatport()
	ipstr = str(node)
	ipsplit = ipstr.split(':')
	ipnum = ipsplit[1]
	if ipnum[4:5] == '0':
		return True 
	else:
		return False

	#if (node=="10.0.0.1:49160"):
	#	return 'found'
	#@app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])

@app.route('/gm')
def getMaster():
	return masternode



#This is the function that was supposed to broadcast to other functions on 
#primary node change
@app.route('/cmk')
def sendChangeMaster():
	#save old masternode
	l = masternode
	#make new list
	newMembersListIds =[x[8:9] for x in memberslist]
	#get this current node
	f = nodek()
	global masternode
	masternode=f
	#remove old master and new master
	if "2" in memberslistIds:
		newMembersListIds.remove("2")
	newMembersListIds.remove(l)

	tks={}

	for z in newMembersListIds:
		a = int(z)
		b = a +5
		c = str(b)
 		req = requests.put('http://10.0.0.2' + z + ':1234' + c + '/cm/' , data = {'val':f})
 		p = req.json()
 		tks[z]=p

 	return str(tks["1"].text)



##This function would have changed the master
@app.route('/cm', methods = ['PUT'])
def changeMaster():
	if request.method == 'PUT':
		x = request.form.get('val')
		global masternode
		masternode=x

		data = {
			'msg' : 'here',
			'error' : masternode
			}
		response = jsonify(data)
		response.status_code = 202
		return response



#TEST RETURNING IP ADDRESS:PORT
@app.route('/testx')
def testx():
	x=whatport()
	return x
	#requests.get('http://localhost:49161/myport')

@app.route('/mast')
def testmaster():
	x = isMasterUser()
	return str(x)



#MAIN KVS PROGRAM
@app.errorhandler(404)
@app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])
def initKVS(key):

	# x = VALUE
	x = request.form.get('val')


	checknode = node()
	whichnode = nodek()
	p=isMasterUser()

	#check if the request came from 
	#a node and not a user
	if checknode ==1:
		#check if this node is the master mode	
		if whichnode==masternode:
			#Because it's the matser simply do regular KVS
			#Do PUT
			if request.method == 'PUT':
				mainput = kvsput(key, x)
				return mainput

			#Do DELETE
			if request.method == 'DELETE':
				theResponse = kvsdel(key, x)
				return theResponse

			#Do GET		
			else:
				theResponse = kvsget(key)
				return theResponse
		else:
			#DO PUT
			if request.method == 'PUT':
				theResponse = kvsput(key, x)
				return theResponse

			#Do DELETE
			if request.method == 'DELETE':
				theResponse = kvsdel(key, x)
				return theResponse

			#Do GET		
			else:
				theResponse = kvsget(key)
				return theResponse
	else:
		#DO PUT
		if request.method == 'PUT':
			if p:
				mainput = kvsput(key, x)
				return mainput
			else:
				theResponse = nodekvsput(key, x)
				lo = str(theResponse)
				#t = int(theResponse.status_code)
				if theResponse==("Fail"):
					x = kvsput(key, x)
					return x
				else:
					return theResponse

		#Do DELETE
		if request.method == 'DELETE':
			theResponse = kvsdel(key, x)
			if p:
				return theResponse
			else:
				secondresponse = nodekvsdel(key, x)
				#t = int(theResponse.status_code)
				po = str(secondresponse)
				if str(secondresponse)==("Fail" or "none"):
					return theResponse
				else:
					return secondresponse
		#Do GET		
		else:
			if p:
				theResponse = kvsget(key)
				return theResponse
			else:
				secondresponse = nodekvsget(key)
				f = str(secondresponse)
				if f == 'Fail':
					x = kvsget(key)
					return x
				else:
					return secondresponse




def nodekvsget(key):
	f = str(key)
	a = int(masternode)
	b = a +5
	c = str(b)
	try:
		r = requests.get('http://10.0.0.2'+ masternode + ':1234' + c + '/kvs/' + f, timeout=.01)
		if r.status_code !=404:
			return 'Fail'
		else:
			data=r.json()
			x = str(data['value'])
			d = kvsput(key, x)
			f = kvsget(key)
			p = str(r)
			if kvs.get(key)!= x:
				return f
			else:
				return f
	except requests.exceptions.RequestException as e:
 		return 'Fail'


# def nodekvsget(key):
# 	f = str(key)
# 	a = int(masternode)
# 	b = a +5
# 	c = str(b)
# 	#try:
# 	r=None
# 	try:
# 		r = requests.get('http://10.0.0.2'+ masternode + ':1234' + c + '/kvs/' + f, timeout=.001)
# 		if r.status_code == 404:
# 			data=r.json()
# 			if str(data['msg']) == 'error':
# 				x = kvsget(key)
# 				return x
# 			elif str(data['msg']) == 'success':
# 				p= str(data['value'])
# 				l=kvsput(key, p)
# 				t=kvsget(p)
# 				return t
# 			else:
# 				return 'Fail'
# 		else:
# 			return 'Fail'
#  	




# 	data=r.json()
# 	x=None
# 	if str(data['value']) is None:
# 		x=None
# 	else:
# 		x = str(data['value'])
# 	d = kvsput(key, x)
# 	f = kvsget(key)
# 	p = str(r)
# 	if kvs.get(key)!= x:
# 		return f
# 	else:
# 		return f



#sends put to master
def nodekvsput(key, x):
	f = str(key)

	a = int(masternode)
	b = a + 5
	c = str(b)

	r=None
	try:
		#s=requests.Session()
		r = requests.put('http://10.0.0.2'+ masternode + ':1234' + c + '/kvs/' + f, data = {'val':x}, timeout=.01)
		if r.status_code ==200:
			x = kvsput(key,x)
			t=kvsput(key,x)
			return t
		elif r.status_code==201:
			m=kvsput(key,x)
			return m
		else:
			r.raise_for_status()
			return 'Fail'
	except requests.exceptions.RequestException as e:
		return 'Fail'
	# except requests.exceptions.HTTPError as e:
	# 	if e.response.status_code!= 201 or 200:
	# 		return 'Fail'
	# 	else:
	# 		return r
	# except requests.exception.Timeout:
	# 	return 'Fail'

	#r = requests.put('http://10.0.0.21:12346/kvs/' + f, data = {'val':x})
	#response=r.json()
	#t = int(r.status_code)


def nodekvsdel(key, x):
	f = str(key)

	a = int(masternode)
	b = a + 5
	c = str(b)

	try:
		r = requests.delete('http://10.0.0.2'+ masternode + ':1234' + c + '/kvs/' + f, data = {'val':x}, timeout=.01)
		if r.status_code != 200 or 404:
			r.raise_for_status()
			return 'Fail'
		else:
			return r
	except requests.exceptions.RequestException as e:
		return 'Fail'

	#r = requests.put('http://10.0.0.21:12346/kvs/' + f, data = {'val':x})
	# t = int(r.status_code)
	# data=r.json()

	# if t == 404:
	# 	return 'none'
	# elif t == 200:
	# 	return r
	# else:
	# 	return 'fail'



 ###############################
## THESE ARE OUR BROADCAST FUNCTIONS####
###############################

# 	def hookbak(request, val, *args, **kwargs):
# 	print ttl 
# 	if request:
# 		global ttl 
# 		if ttl > 0:
# 			timeToLive = str(ttl)
# 			try:
# 				res = requests.put(request.pop() + "?ttl=" + timeToLive, data = {'val':val}, timeout = 5)
# 				return "do it"
# 			except requests.exceptions.Timeout:
# 				print "hook timeout \n"
# 				return "hook failed"
# 		#else: return "no mo\n"
# 	else:
# 		return "No mo\n"

# def bcast(members, val):
# 	if not members:
# 		return "all done\n"
# 	global ttl
# 	ttl = int(ttl)
# 	ttl -= 1 
# 	if ttl > 0:
# 		timeToLive = str(ttl)
# 		member = members.pop()
# 		try: 
# 			print member + " requester space\n"
# 			resp = requests.put(member + "?ttl=" + timeToLive, data = {'val':val}, timeout = 5, hooks = {'response': bcast(members, val)})
# 			#'members':members
# 			return "titys!"
# 		except requests.exceptions.Timeout:
# 			#print members
# 			print "timedout\n"
# 			return "dick!"
# 	else:
# 		return "stop broadcasting"



# #MAIN KVS PROGRAM
# @app.route('/kvs/<key>', methods = ['PUT', 'GET', 'DELETE'])
# def initKVS(key):
# 	#hooks = {request: bcast}

# 	#if empty request.info: return 
# 	# x = VALUE

# 	x = request.form.get('val')

# 	# creating the urls for puts
# 	urls = [i + '/kvs/' + key for i in memberslist]
# 	print memberslist
# 	print urls
# 	reals = [j.encode('ascii') for j in urls]
# 	print reals

# 	if request.method == 'PUT':

# 		global ttl 
# 		ttl = request.args.get('ttl')
# 		if node() == 0:
# 			ttl = 5
# 			res = kvsput(key, x)
# 			bcast(reals, x)
# 			return res
# 		#elif ttl > 0:
# 			#res = kvsput(key, x) 
# 			#bcast(reals, x)
# 			#return res
# 		else:
# 			res = kvsput(key, x) 
# 			#bcast(reals, x)
# 			return res
# 			#print "ttl: " + ttl
# 			return ttl
# 	elif request.method == 'DELETE':
# 		return kvsdel(key, x)
# 	elif request.method == 'GET':
# 		return kvsget(key)

# def kvsput(key, x):
# 	global ttl
# 	# ttl = int(ttl)
# 	# ttl -= 1
# 	timeToLive = ttl
#  	if timeToLive > 0:
#  		print ttl
# 		if kvs.get(key) == None:
# 			kvs[key] = x
# 			data = {
# 			'replaced' : 0,
# 			'msg' : 'success',
# 			'membersIDS': memberslistIds,
# 			'master':masternode
# 			}
# 			response = jsonify(data)
# 			response.status_code = 201
# 			return response

# 			#replace value of key with new value	
# 		else:
# 			kvs[key] = x
# 			data = {
# 			'replaced' : 1,
# 			'msg' : 'success'
# 			}
# 			response = jsonify(data)
# 			response.status_code = 200
# 			return response


	

def kvsget(key):
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

def kvsdel(key,x):
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

#insert into kvs
def kvsput(key, x):
	if kvs.get(key) == None:
			kvs[key] = x
			#r = requests.get('http://10.0.0.22:12347/testx')
			data = {
			'replaced' : 0,
			'msg' : 'success'
			}
			#payload = {'val': x}
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

@app.route('/mem')
def mem():
	for z in memberslistIds:
 		a = int(z)
		b = a +5
		c = str(b)
		return c


#def checkT(key, value):

#def checkmaster(key):
#	cmaster=requests.get(https://localhost:49160)


if __name__ == '__main__':
	#x = 'asd'
	#f = hash(x, 10)
	#print f
	app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
	app.debug = True
	app.run(host=ip, port=int(port))



