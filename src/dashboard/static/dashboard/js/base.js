const DASHBOARD = '/dashboard/';
const TABLE = '/table/';
const REPORTS = '/reports/';
const NOTIFICATION_BOX = document.querySelector('.right .recent-updates .updates');

function reportDataUpdate(inputData){
	switch(window.location.pathname) {
		case DASHBOARD:
			func = function(data) {
				// вызываемые функции определены в right.js и dashboard.js
				changeProgresTabsValue(data);
				changeAnlyticsValue(data);
			};
			break;
		case TABLE:
			func = function(data) {
				changeAnlyticsValue(data);
			};
			break;
		case REPORTS:
			func = function(data) {
				changeAnlyticsValue(data);
			};
			break;
		default:
			func = function(data) {
				console.log('Error! Pathname: ' + window.location.pathname);
				console.log(data);
			}
			break;
	}
	func(inputData);
};

function startWebSocket() {
	const URL = 'ws://' + window.location.hostname + ':80/ws/log/';
	const SOCKET = new WebSocket(URL);

	SOCKET.onmessage = function(event){
	// Processing new messages in the group
		let message = JSON.parse(event.data)
		if (message.type === "reports"){
			reportDataUpdate(message)
		}
		else if(message.type === "notification"){
			createNotify(message, NOTIFICATION_BOX);
		}
		else if(message.type === "count"){
			counterUpdate(message);
		}
		else {
			// pass
		};
	};

	SOCKET.onclose = function(){
	// Try to reconnect in 5 seconds
	setTimeout(function() {startWebSocket()}, 5000);
	};
};
startWebSocket()