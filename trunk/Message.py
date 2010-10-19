import datetime

class Message:
	"""
	A single message object stored on the chat server.
	"""
	htmlFormatString="<div id='{4}' class='message  {2}'><div class='messageBody'>{3}</div><div class=time>{1}</div><div class=name>{0}</div></div>"	
	htmlError = "<span class='error'>Message hidden due to HTML content</span>"
	lengthError =  "<span class='error'>Message hidden due to being above 250 char limit</span>"

	def __init__(self, username, body, cssClass, Id):
		body = self._sanitize(body)
		self.username = username
		self.body = str(body)
		self.time = datetime.datetime.now()
		self.cssClass = cssClass
		self.Id = Id #uniquely identifies the message for use on the client. used to set the divId to 'msgX' where X is the numeric Id
				
	def _sanitize(self, message):
		if not message : return ''
		if message.find('<') != -1 or message.find('>') != -1 : return self.htmlError
		if len(message) > 250: return self.lengthError
		return message

	def getHTML(self, username=''):
		aditionalCssClass = self.cssClass + ' ' + ((self.username==username) and 'mine' or '  ') #add class 'messagemine' if its my message
		divId = 'msg{0}'.format(self.Id)
		html = self.htmlFormatString.format(self.username, self.time.time().__str__()[:8], aditionalCssClass, self.body, divId)
		return htmlWrapper(html, divId)
	



class htmlWrapper:
	"""
	A html object to be displayed by the client
	html is a string that should be div tags with html inside.  The divId must be both specified in the HTML and passed in to the contructor.
	a ServerResponse retains a list of these objects to be returned to the client
	"""
	def __init__(self, html, divId):
		
		self.html = html
		self.divId = divId

	def serialize(self):
		 return {'divId' : self.divId, 'html' : self.html}
	
