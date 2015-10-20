## WebChatServer ##

The WebChatServer class is found in the WebChatServer.py file along with the MyHandler Class.

WebChatServer extends the base HTTPServer class, and has a single additional property
.ChatServer
which hold a ChatServer instance, which handles the messaging functionality.

The Myhandler class has two methods to handle GET and POST requests from the clients respectively.

doGET:
Looks at the url requested and uses the ending to determine if a .css or .js file was requested.  If this is the case main.js or style.cs is returned.
If the user is not logged in, then login.html is returned,
otherwise chat.html is returned.

doPost and HandleRequest:
doPost passes the data from the client request to HandleRequest.  Data is just a string (the user input), and an action type.
HandleRequest uses the action type to determine which method on the chat server to call (may be more than one)
Responses from the ChatServer (ServerResponse objects) are added to a list, which is then serialized and sent back to the client.