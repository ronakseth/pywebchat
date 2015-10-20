# Installation and use #

To start using PyWebChat, download the pywebchat.tar.gz file from the downloads section.

untar the file to a directory using "tar -xvwzf pywebchat.tar.gz" (linux)

To run the server, cd into the newly created pywebchat directory and execute
$ python ChatSever.py

Since the server runs on port 80, you may need to prefix the command with 'su' to have the permissions to listen on the port.

## Changing the server port ##
For the moment, to change the port the server runs on, you'll have to go in and edit the source by hand.

Open the ChatServer.py file in a text editor and find the startServer function.
find the line that looks like :
`webServer = WebChatServer.MiniWebServer(('', 80), MyHandler)`
and change the number 80 to whatever port you want the server to run on.

## Stopping the server ##

To stop the server, hit Ctrl+C in the terminal window that the server was run from.

## Connecting ##
point your browser to your IP address ('localhost' if you are on the server that is running pywebchat) and you will be presented with the login page.
(adding a page to the url like '/chat.py' isn't required, as PyWebServer just ignores it and server up the required page anyway.

Enter a username and press enter to get started.
Others on your network can access the server in the same way.

To send a message just type in the box and hit enter to send.
To logout hit the logout link