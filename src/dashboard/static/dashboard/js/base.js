const DASHBOARD = '/dashboard/';
const TABLE = '/table/';
const REPORTS = '/reports/';
const NOTIFICATION_BOX = document.querySelector('.right .recent-updates .updates');
returnedNotificationSettings = JSON.parse(document.querySelector("#raw-burned-notification-settings").textContent);
burnedNotificationSettings = JSON.parse(document.querySelector("#raw-returned-notification-setting").textContent);

function playAudio(audioFile){
	audioFile.play();
	audioFile.currentTime = 0;
};

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
		let message = JSON.parse(event.data);

		if (message.type === "reports"){
			reportDataUpdate(message);
		}
		else if(message.type === "notification"){
			if (message.subtype === 'new') {
				playAudio(notificationAudio);
			} else if (message.subtype === 'burned' || message.subtype === 'returned') {
				playAudio(alarmAudio);
			} else if (message.subtype === 'updated' && message.issue.step === groupStep) {
				playAudio(notificationAudio);
			} else {
				// pass
			}
			createNotify(message, NOTIFICATION_BOX);
		}
		else if(message.type === "count"){
			valueCounterUpdate(message);
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