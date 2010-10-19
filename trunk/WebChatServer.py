import string,cgi,urlparse,time
from os import curdir, sep, environ
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import types
import json

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
    def handleMessage(self, query, IP):
		requestType = query["requestType"].pop()
		try:
			text = query['userinput'].pop()
		except KeyError:
			text = ''		
		responseList = []		
		
		if  requestType == 'message':
			response = self.server.chatServer.sendMessage(IP,text)
			response and responseList.append(response.serialize())
			response = self.server.chatServer.getNewMessages(IP)
			response and responseList.append(response.serialize())
		elif requestType == 'update':
			response = self.server.chatServer.getNewMessages(IP)
			response and responseList.append(response.serialize())
		elif requestType == 'updateForced':
			response = self.server.chatServer.getNewMessages(IP, force=True)
			response and responseList.append(response.serialize())
		elif requestType== 'logout':
			response = self.server.chatServer.logout(IP)
			response and responseList.append(response.serialize())
		elif requestType=='login':
			response = self.server.chatServer.login(text, IP)
			response and responseList.append(response.serialize())
		elif requestType=='search':
			response = self.server.chatServer.search(IP,text)
			response and responseList.append(response.serialize())
		#while we're here get an uptodate list of who's online
		response = self.server.chatServer.getOnlineList()
		response and responseList.append(response.serialize())
		#return responses to the client
		json.dump(responseList, self.wfile)

				
				
	
    def do_GET(self):
	"""
	ignore url and return the basic page
	"""
        try:
		if self.path.endswith("css"):
			page = 'style.css'
		elif self.path.endswith(".js"):
			page = 'main.js'
		else:
			page = self.server.chatServer.isClientRegistered(self.address_string()) and 'chat.html' or 'login.html'
		f = open(curdir + sep + page)
                self.send_response(200)
                self.send_header('Content-type','text/html')
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
        #global rootnode
        clientsIP = self.address_string()
        contentType, pDict = cgi.parse_header(self.headers.getheader('content-type'))
	contentLength, pDict = cgi.parse_header(self.headers.getheader('content-length'))
	if contentType == 'multipart/form-data':
           	query=cgi.parse_multipart(self.rfile, parseDict)
	else:
		#TODO The else should be 'xxx-application'
		qstring = self.rfile.read(int(contentLength)) 
		query=urlparse.parse_qs(qstring)
	self.end_headers()
	self.handleMessage(query, clientsIP)


	

	
            
        


