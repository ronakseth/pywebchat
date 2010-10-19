from Message import *
import types

class ServerResponse(object):
	"""
	Returned to the client in json format in response to a client request
	.target = id of div that contents should be added to
	.action = 'replace' | 'append' | 'prepend' | 'delete'  : method of addition to the target div
	.contents = List of htmlWrapper objects

	target divs are:
	messages : area for messages to be displayed
	notication : area for non-error notifications
	error : errors
	"""

	def __init__(self, target, action, contents, isError=False):
		self.target = ''
		self.action = ''
		self.isError = isError
		self.contents =  (type(contents) is types.ListType) and contents or [contents]

	def serialize(self):
		html = [msg.serialize() for msg in self.contents]
		return { 'target' : self.target, 'action' : self.action, 'isError' : self.isError, 'content' : html}
	
	def addToContents(self, htmlWrapper):
		self.contents.append(htmlWrapper)

class ServerResponseMessages(ServerResponse):
	"""
	The response returned by getNewMessages
	"""
	def __init__(self, messages):
		self.target = 'messages'
		self.action = 'prepend'
		self.isError = False
		self.contents = (type(messages) is types.ListType) and messages or [messages]

class ServerResponseSearchMessages(ServerResponse):
	"""
	The server response returned by search messages if there are some messages to be returned
	"""
	def __init__(self, messages):
		self.target = 'searchresults'
		self.action = 'replace'
		self.isError = False
		self.contents = (type(messages) is types.ListType) and messages or [messages]

class ServerResponseSearchNoMessages(ServerResponse):
	"""
	The server response returned by search messages if there are no messages to be returned
	"""
	def __init__(self, searchString):
		self.target = 'searchresults'
		self.action = 'replace'
		self.isError = False
		self.contents = [htmlWrapper("<div id=noresults>'{0}' not found</div>".format(searchString), 'noresults')]

class ServerResponseOnlineList(ServerResponse):
	def __init__(self, onlinehtml):
		self.target = 'online'
		self.action = 'replace'
		self.isError = False
		self.contents = [onlinehtml]
		
class ServerResponseNotification(ServerResponse):
	def __init__(self):
		self.target = 'notification'
		self.action = 'replace'
		self.isError = False

class ServerResponseLoginSuccess(ServerResponseNotification):
	def __init__(self, username):
		ServerResponseNotification.__init__(self)
		self.contents = [htmlWrapper('<div id=loginsuccess><a href=/chat.html>{0} registered, click here to chat</a></div>'.format(username), 'loginsuccess')]

class ServerResponseLogoutSuccess(ServerResponseNotification):
	def __init__(self, username):
		ServerResponseNotification.__init__(self)
		self.contents = [htmlWrapper('<div id=logoutsuccess><a href=/chat.html>{0} successfully logged out</a>>/div>'.format(username), 'logoutsuccess')]



class ServerResponseError(ServerResponse):
	def __init__(self):		
		self.target = 'error'#dump stuff in the error div
		self.action = 'replace'
		self.isError = True

class ServerResponseErrorNotLoggedIn(ServerResponseError):
	def __init__(self):
		ServerResponseError.__init__(self)
		self.contents = [htmlWrapper('<div id=loginerror>You must be logged in to send and receive messages</div>' , 'loginerror')]
		
class ServerResponseErrorMessageTooLong(ServerResponseError):
	def __init__(self):
		ServerResponseError.__init__(self)
		self.contents = [htmlWrapper('<div id=messageerror>Message must be < 250 chars</div>' , 'messageerror')]

class ServerResponseErrorMessageHasHTML(ServerResponseError):
	def __init__(self):
		ServerResponseError.__init__(self)
		self.contents = [htmlWrapper('<div id=messageerror>Message cannot contain HTML tags \'<\' or \'>\'</div>' , 'messageerror')]
