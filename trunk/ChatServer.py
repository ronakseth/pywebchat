import time
import WebChatServer
from ServerResponse import *
import datetime
from Message import *
import uuid

class ChatServer:
		"""
		Chat server that handles sending and receiving of messages from several clients
		All methods called from the webserver must return a  ServerResponse object, or False if no response is required

		Methods available to the webserver are

		getNewMessages
		sendMessage
		getOnlineList
		login
		logout

		
		"""
		def __init__(self, IP, serverName='Server', DEBUGGING=False):
			self.DEBUGGING = DEBUGGING
			self.messages = []		#stores all the messages received so far.
			self.clients = {}		#maps client Ips to client data
			self.usernamesInUse = set()	#new usernames can be checked here to ensure uniqueness.
			self.serverIP = IP			
			self.serverName = serverName
			self.messageCounter = 1
			self.login(serverName, IP) #register the server so we can send messages
			print 'Chat server started'

		def login(self, username, IP ):
			if not self.clients.has_key(IP) and  self.validUsername(username):
				self.clients[IP] = ClientData(username)
				self.usernamesInUse.add(username)
				if (username != self.serverName):self.sendMessage(self.serverIP, "{0} joined the room".format(username))
				return ServerResponseLoginSuccess(username)
			return ServerResponseErrorNotLoggedIn()# TODO: change to a 'invalid username error'
			
		def logout(self,  IP):
				if not (self.clients.has_key(IP)): return 
				username = self.clients[IP].username
				del self.clients[IP]
				self.usernamesInUse.discard(username)
				self.sendMessage(self.serverIP, "{0} left the room".format(username))
				return ServerResponseLogoutSuccess(username)					

		def sendMessage(self, IP, messageString):
			if not (self.clients.has_key(IP)): return ServerResponseErrorNotLoggedIn()
			if (not messageString) or messageString.isspace(): return False
			self.messageCounter += 1
			cssClass = (self.serverIP == IP and 'notification' or ' ')#thislogic should really be shipped out to the message
			self.messages.append(Message(self.clients[IP].username, messageString, cssClass, self.messageCounter))
			return False #success so no need for a full response
			
		def getNewMessages(self, IP, force=False):				
			if not (self.clients.has_key(IP)): return ServerResponseErrorNotLoggedIn()
			lastUpdated = (force and  datetime.datetime.now() - datetime.timedelta(minutes=30) or self.clients[IP].lastUpdated)
			username = self.clients[IP].username			
			messageList =  [msg.getHTML(username) for msg in self.messages if (msg.time > lastUpdated)]
			self.updateClient(IP)
			if (messageList == []): return False #no messages so no response needed
			return ServerResponseMessages(messageList)

		def getOnlineList(self):
			html = "".join([(x + '</br>') for x in self.usernamesInUse if (x != self.serverName)])
			wrapped = htmlWrapper('<div id=onlineNames>{0}<div>'.format(html), 'onlineNames')
			return ServerResponseOnlineList(wrapped)
				
		def validUsername(self, uname):
			return (uname and uname.isalpha() and len(uname) < 15 and len(uname) > 2 and not (uname in self.usernamesInUse))

		def updateClient(self, IP):
			self.clients[IP].lastUpdated = datetime.datetime.now()

		def isClientRegistered(self, IP):
			return self.clients.has_key(IP)

		def search(self, IP, searchString):
			if not (self.clients.has_key(IP)): return ServerResponseErrorNotLoggedIn()
			username = self.clients[IP].username
			messageList = [msg.getHTML(username, idPrefix='srchmsg') for msg in self.messages if searchString in msg.body]
			return messageList and ServerResponseSearchMessages(messageList) or ServerResponseSearchNoMessages(searchString)

		def _getNewId(self):
			return uuid.uuid4()

class ClientData:
	"""
	Stores the required data about a client
	"""
	def __init__(self, username):
		self.username = username
		self.lastUpdated = datetime.datetime.now() - datetime.timedelta(minutes=30) #set last updated to ten minutes ago.

def startServer():
	MyHandler = WebChatServer.MyHandler
        webServer = WebChatServer.MiniWebServer(('', 80), MyHandler)
	chatServer = ChatServer('www.mydomain.com')
	webServer.chatServer = chatServer
	print 'Starting the WebServer'	
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		print 'exiting (received ^C)'		
		webServer.socket.close()
if __name__ == "__main__":
	startServer()	
	

