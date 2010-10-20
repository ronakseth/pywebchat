import string,cgi,urlparse,time
from os import curdir, sep, environ
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import types
import json
import uuid


class MiniWebServer(HTTPServer):
	chatServer = ''

class MyHandler(BaseHTTPRequestHandler):
    """
    calls to the chat server return False (no response) or a server response object.
    these are serialized and added to a list.
    this list is then returned to the client

    Callable methods on the Chat server are
    	getNewMessages
	sendMessage
	getOnlineList
	login
	logout
    Request Types that the Web server should accept are
	login
	logout
	message
	update
	updateForced
    All request types other than logout/login should also include a getOnlineList call
    message should include an updatecall
    """
    def handleMessage(self, query):
		responseList = []
		flag, ssid = self.getSSID()
		if not flag: #cookie is invalid and user has been sent a new one, so return a message that the user has to login again
			responseList.append(self.server.chatServer.getNewMessages('foo'))#try and get message with an unregistered ID and we'll get the login response
		else:#user has a valid ssid.. so try the request	
			requestType = query["requestType"].pop()
			try:
				text = query['userinput'].pop()
			except KeyError:
				text = ''		
			if  requestType == 'message':
				response = self.server.chatServer.sendMessage(ssid,text)
				response and responseList.append(response.serialize())
				response = self.server.chatServer.getNewMessages(ssid)
				response and responseList.append(response.serialize())
			elif requestType == 'update':
				response = self.server.chatServer.getNewMessages(ssid)
				response and responseList.append(response.serialize())
			elif requestType == 'updateForced':
				response = self.server.chatServer.getNewMessages(ssid, force=True)
				response and responseList.append(response.serialize())
			elif requestType== 'logout':
				response = self.server.chatServer.logout(ssid)
				response and responseList.append(response.serialize())
			elif requestType=='login':
				print 'logging in user' + text + ssid
				response = self.server.chatServer.login(text, ssid)
				response and responseList.append(response.serialize())
			elif requestType=='search':
				response = self.server.chatServer.search(ssid,text)
				response and responseList.append(response.serialize())
		#while we're here get an uptodate list of who's online
		response = self.server.chatServer.getOnlineList()
		response and responseList.append(response.serialize())
		#return responses to the client
		json.dump(responseList, self.wfile)

    def getSSID(self):
	"""
	parses the header to grab a cookie from the client and get the SSID
	If no cookie is found, generates a new one and sends to the client.
	returns a tuple of 'valid cookie found' flag, and the ssid
	"""
	try:#check if the client has a cookie
		cookie, pdict = cgi.parse_header(self.headers.getheader('Cookie'))
		ssid = cookie.split('=')[1]
		if len(ssid) != 32: raise Exception('invalid ssid in cookie')
	except:#generate a new cookie and send to the client
		ssid = uuid.uuid4().hex
		self.send_header('Set-Cookie', 'ssid=' +ssid  )
		return (False, ssid)	
	return (True, ssid)
	
    def do_GET(self):
	"""
	ignore url and return the basic page
	"""
        try:
		self.send_response(200)
                self.send_header('Content-type','text/html')
		flag, ssid = self.getSSID()#throw the client a cookie if they don't already have one

		if self.path.endswith("css"):
			page = 'style.css'
		elif self.path.endswith(".js"):
			page = 'main.js'
		else:
			page = self.server.chatServer.isClientRegistered(ssid) and 'chat.html' or 'login.html'
		f = open(curdir + sep + page)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
                            
        except IOError:
        	self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
	"""
	grab 'command' from the form data and send to server.
	"""
        contentType, pDict = cgi.parse_header(self.headers.getheader('content-type'))
	contentLength, pDict = cgi.parse_header(self.headers.getheader('content-length'))
	
	if contentType == 'multipart/form-data':
           	query=cgi.parse_multipart(self.rfile, parseDict)
	else:
		#TODO The else should be 'xxx-application'
		qstring = self.rfile.read(int(contentLength)) 
		query=urlparse.parse_qs(qstring)
	self.end_headers()
	self.handleMessage(query)


	

	
            
        


