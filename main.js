var awaitingSearchResponse = false;

function getMessages(){sendMessage('none', 'update');}
function getMessagesForced(){sendMessage('none' ,'updateForced');}
function logout(){sendMessage('none', 'logout');}
function dosearch(){
var msg = $("#searchtext").val();
	if (awaitingSearchResponse != false){ return 0;}
	 if (msg.length > 2){ 
		sendMessage( msg,'search');
	}else{
		$('#searchresults').html('');}}
function handleResponse(response){//handles a single ServerResponse object
	var target = '#' + response['target'];
	var action = response['action'];
	var content = response['content'];
	var addedDivs = [];//maintains a list of the ids of divs that are returned in the response
	if (action == 'prepend')
	{
		for (i in content){
			$(target).prepend(content[i]['html']);
			addedDivs.push(content[i].divId);	
			}
	}
	else if(action == 'append')
	{
		for (i in content){
			$(target).prepend(content[i]['html']);
			addedDivs.push(content[i].divId);	
			}
	}
	else if (action == 'delete')
	{
		var x = 1; //implement later
	}
	else if (action == 'replace'){
		var replacementText = '';
		for (i in content){
			replacementText += content[i]['html'];
			addedDivs.push(content[i].divId);
		}
		$(target).html(replacementText);
	}

	for (i in addedDivs)
	{
		$('#' + addedDivs[i]).fadeTo("slow",1.0);
	}

	if (target == '#searchresults'){awaitingSearchResponse = false;}//if this is a response to a search, reset the flag
	
}



function sendMessage(msg, requestType){
	$.post('chat.html', {"userinput" : msg, "requestType" : requestType },
		function(data) {
			var result = jQuery.parseJSON(data);
			for (i in result){
				handleResponse(result[i]);
			}
		 });
	$('.message').hover(function(){$(this).addClass('highlight');}, function(){$(this).removeClass('highlight');});
}

