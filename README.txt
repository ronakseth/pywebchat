#
#  PyWebChat README
# 
#  Released under the GPLv3 public licence
#  t33n4n@gmail.com
#
#
#
To start using PyWebChat, download the pywebchat.tar.gz file from the downloads section.
http://code.google.com/p/pywebchat/downloads/list

untar the file to a directory using "tar -xvwzf pywebchat.tar.gz" (linux) or winrar or similar (windows)

# Running the server

LINUX:
To run the server, cd into the newly created pywebchat directory and execute 
$ python ChatSever.py

Since the server runs on port 80, you may need to prefix the command with 'su' to have the permissions to listen on the port.

WINDOWS:
depending on the setup, windows users should copy the files from the extracted tarball to their python directory
e.g. C:\Python2.7\

Then from the python command line, run

$ import ChatServer
$ ChatServer.startServer()

you may need to run python as an administrator to have permissions to bind on the port.

# Changing the default port

For the moment, to change the port the server runs on, you'll have to go in and edit the source by hand.

Open the ChatServer.py file in a text editor and find the startServer function. find the line that looks like : 
webServer = WebChatServer.MiniWebServer(('', 80), MyHandler) and change the number 80 to whatever port you want the server to run on.

# Stopping the server

To stop the server, hit Ctrl+C in the terminal window that the server was run from.
Connecting

# Connecting to the server

point your browser to your IP address ('localhost' if you are on the server that is running pywebchat) and you will be presented with the login page. (adding a page to the url like '/chat.py' isn't required, as PyWebServer? just ignores it and server up the required page anyway.

Enter a username and press enter to get started. Others on your network can access the server in the same way.

To send a message just type in the box and hit enter to send. To logout hit the logout link.
The search box on the right of the page is buggy, but just typing in the box should search all the messages sent so far for one's that match the string entered.

email t33n4n@gmail.com with bugs/suggestions
