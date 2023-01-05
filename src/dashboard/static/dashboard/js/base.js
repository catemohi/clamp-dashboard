function start_chat_ws() {
	let url = 'ws://' + window.location.hostname + ':80/ws/log/';
	let socket = new WebSocket(url);
	let notification_box = document.querySelector('.right .recent-updates .updates');

	socket.onmessage = function(event){
	// Processing new messages in the group
		let notify = JSON.parse(event.data)
		createNotify(notify, notification_box);
	};

	socket.onclose = function(){
	// Try to reconnect in 5 seconds
	setTimeout(function() {start_chat_ws()}, 5000);
	};
};

function log_pathparth() {
    console.log(window.location.pathname)
}

log_pathparth()