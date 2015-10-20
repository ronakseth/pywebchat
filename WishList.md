This page records features that it would be nice to see added to PyWebChat.
If you think you can help with a feature/task, email t33n4n@gmail.com

# ToDo: #

  * Allow users to specify the port the server runs on with a command line argument.
> e.g. $python ChatServer.py 80
> > DONE

  * Design a logo and add it to the login.html and chat.html markup

  * Add additional stylesheets (CSS) and allow the user to choose which one to use with a command line argument when the server is started

  * Add a search(searchstring) method to the ChatServer class that searches existing messages for a string, and returns the messages found in a ServerResponse object. (This will be used later in a search feature to be added)
    * 19/10/2010: An instant search function has been included, but needs a bit more work:
      * Have a single box for both search and chat text input, with a button to switch the modes, rather than a completely separate search area (this should be a pretty small job since all of the functionality is there.
> > > DONE

  * Add a getMessageBy(username) method to the ChatServer class that returns all the messages by user 'username'. (This will be used later in a feature where clicking a username displays all the message by that user)

  * add CSS for the 'error' and 'notification' divs so that they display in the right place.

  * add a README.txt to the tarball with the useage instructions from this wiki

> > DONE

  * Add a command directive '@' that causes the following word to be interpreted as a command.. e.g. @logout to logout, @clear to clear the screen of message @get to force an update of all messages in the last 10 minutes or so.

> This would require a special command handler class.. if the first char of a message is @, the remaining string is passed into the command handler and the appropriate server response object returned.