## main.js ##

This file holds the main javascript functions for the client.

The main functions are sendMessage and handleResponse

sendMessage takes a string and an action type and posts them up to the server.
The response from the server is parsed as a JSON string and the resulting list of ServerResponse objects are passed one at a time to the handleResponse function.

handleResponse performs the action specified in the response on the target div also specified in the response.
action types can be: prepend | append |replace | delete (not currently implemented
handleresponse maintains a list of the Ids of divs that were added and can perform an action on these divs, such as a nice appearance transition.