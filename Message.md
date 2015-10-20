## Message ##

The Message class is found in the Message.py file along with the htmlWrapper class.

Message stored the content, username, time and associated cssClass of a message.

the getHtml function returns the message in html format.
The username of the user requesting the message is passed in to getHTML to allow for different formatting of the user's own messages.  Messages from the server are also formatted differently.

the htmlWrapper class wraps any html string and stores the (unique)id of the div containing the html.
This is so that the client can add or remove the html element easily and know the id of the element that was effected, which cuts down on the js required on the client side.

A ServerResponse instance maintains a list of these htmlWrapper objects in its contents field to be returned to the client.