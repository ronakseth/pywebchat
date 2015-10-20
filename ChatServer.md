The ChatServer class is found in ChatServer.py and stores all the messages and user data.

This class handles the sending and receiving of messages, as well as logging clients in and out.


.messages
Messages are stored as message objects in a simple list

.usernamesinuse
Usernames are stored in a set to quickly check if a username is in use when a new user tries to log in.

.clients
clients is a dictionary mapping a client's IP address to their username.  Ip addresses are assumed to be unique for this purpose

TODO: details about the class and how it works