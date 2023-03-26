// changet heme
const themeToggler = document.querySelector(".theme-toggler");
const menuBtn = document.querySelector(".menu-btn");

themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-var');

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
    
    if (themeToggler.querySelector('span:nth-child(2)').classList.contains('active')) {
        document.cookie = "theme=dark; path=/;";
    } else {
        document.cookie = "theme=white; path=/;";
    }

})

document.querySelector('.accordion').addEventListener('click', (event) => {
    document.querySelector('.panel').classList.toggle('hide');
});

// show sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

//close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})


if (localStorage.layoutSwitch === 'true') {
    document.body.classList.toggle('dark-theme-var');
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
}

function fadeIn(el, speed) {
	// Fade in block
	var step = 1 / speed;
	var interval = setInterval(function() {
		if (+el.style.opacity >= 1)
			clearInterval(interval);
			
		el.style.opacity = + el.style.opacity + step;
	}, speed / 1000);
}

function createNotify(notify, notifyParent) {
    let notificationText
	// Creating a new block
	let update_item = document.createElement('div');
	update_item.className = "update";
	update_item.style.opacity = "0";

	let img_box = document.createElement('div');
	img_box.className = "profile-photo";
	img = document.createElement('img');
	// let img_link determined from django template
	img.src = img_link

	let message = document.createElement('div');
	message.className = "message";

	let textBox = document.createElement('p');
    textBox.className = "text-massage";
	let emoji = document.createElement('span');
    let text = document.createElement('span');

    if (notify.subtype === 'burned') {
        emoji.innerText = '🧨';
        emoji.className = "emoji-span";
    } else if (notify.subtype === 'returned') {
        emoji.innerText = '✉️'; 
        emoji.className = "emoji-span";
    } else if (notify.issue.vip_contragent === true) {
        emoji.innerText = '❤️';
        emoji.className = "emoji-span";
    } else {
        // pass
    };
    
	text.innerHTML = '<a href="' + notify.issue.url_issue + '">'+ notify.text + '</a>';
    textBox.appendChild(emoji);
    textBox.appendChild(text);
	let time = document.createElement('small');
	time.className = "text-muted";
	time.innerText = (new Intl.DateTimeFormat("ru", options).format(new Date(notify.time)));
    

	message.appendChild(textBox);
	message.appendChild(time);
	img_box.appendChild(img)
	update_item.appendChild(img_box);
	update_item.appendChild(message);
	notifyParent.insertBefore(update_item, notifyParent.firstElementChild);
	fadeIn(update_item, 200);
};

function parsingInt(textString) {
    return parseInt(textString.replace(/^(0$|-?[1-9]\d*(\.\d*[1-9]$)?|-?0\.\d*[1-9])$/, ''));
};

function changeAnalytics() {
    let Analytics = [document.querySelector(".sl-first-line"),
                     document.querySelector(".sl-vip-line"),
                     document.querySelector(".sl-general"),
                     document.querySelector(".mttr"),
                     document.querySelector(".flr"),
                     document.querySelector(".aht")];


    Analytics.forEach(function modifyPercentRatings(module) {


        let daylySL = module.querySelector(".dayly_sl *")
        if (daylySL != null) {
            let valueSL= parsingInt(daylySL.textContent);
			// minSuccessSL прописана в контексте base.html и тянется с БД
            if (valueSL >= minSuccessSL) {
                daylySL.classList.add("success");
            }
            else {
                daylySL.classList.add("danger");
            }
        }
        let  WeeklySL = module.querySelector(".weekly_sl *")
        if ( WeeklySL != null) {
            let valueSL= parsingInt( WeeklySL.textContent);
			// minSuccessSL прописана в контексте base.html и тянется с БД
            if (valueSL >= minSuccessSL) {
                 WeeklySL.classList.add("success");
            }
            else {
                 WeeklySL.classList.add("danger");
            }
        }
        let  MountlySl = module.querySelector(".mountly_sl *")
        if ( MountlySl != null) {
            let valueSL= parsingInt( MountlySl.textContent);
			// minSuccessSL прописана в контексте base.html и тянется с БД
            if (valueSL >= minSuccessSL) {
                 MountlySl.classList.add("success");
            }
            else {
                 MountlySl.classList.add("danger");
            }
        }
        let daylyMTTR = module.querySelector(".dayly_mttr *")
        if (daylyMTTR != null) {
            let valueMTTR= parsingInt(daylyMTTR.textContent);
			// maxSuccessMTTR прописана в контексте base.html и тянется с БД
            if (valueMTTR <= maxSuccessMTTR) {
                daylyMTTR.classList.add("success");
            }
            else {
                daylyMTTR.classList.add("danger");
            }
        }
        let weeklyMTTR = module.querySelector(".weekly_mttr *")
        if (weeklyMTTR != null) {
            let valueMTTR= parsingInt(weeklyMTTR.textContent);
			// maxSuccessMTTR прописана в контексте base.html и тянется с БД
            if (valueMTTR <= maxSuccessMTTR) {
                weeklyMTTR.classList.add("success");
            }
            else {
                weeklyMTTR.classList.add("danger");
            }
        }
        let mountlyMTTR = module.querySelector(".mountly_mttr *")
        if (mountlyMTTR != null) {
            let valueMTTR= parsingInt(mountlyMTTR.textContent);
			// maxSuccessMTTR прописана в контексте base.html и тянется с БД
            if (valueMTTR <= maxSuccessMTTR) {
                mountlyMTTR.classList.add("success");
            }
            else {
                mountlyMTTR.classList.add("danger");
            }
        }
        let daylyFLR = module.querySelector(".dayly_flr *")
        if (daylyFLR != null) {
            let valueFLR= parsingInt(daylyFLR.textContent);
			// minSuccessFLR прописана в контексте base.html и тянется с БД
            if (valueFLR >= minSuccessFLR) {
                daylyFLR.classList.add("success");
            }
            else {
                daylyFLR.classList.add("danger");
            }
        }
        let weeklyFLR = module.querySelector(".weekly_flr *")
        if (weeklyFLR != null) {
            let valueFLR= parsingInt(weeklyFLR.textContent);
			// minSuccessFLR прописана в контексте base.html и тянется с БД
            if (valueFLR >= minSuccessFLR) {
                weeklyFLR.classList.add("success");
            }
            else {
                weeklyFLR.classList.add("danger");
            }
        }
        let mountlyFLR = module.querySelector(".mountly_flr *")
        if (mountlyFLR != null) {
            let valueFLR= parsingInt(mountlyFLR.textContent);
			// minSuccessFLR прописана в контексте base.html и тянется с БД
            if (valueFLR >= minSuccessFLR) {
                mountlyFLR.classList.add("success");
            }
            else {
                mountlyFLR.classList.add("danger");
            }
        }
        let daylyAHT = module.querySelector(".dayly_aht *")
        if (daylyAHT != null) {
            let valueAHT= parsingInt(daylyAHT.textContent);
			// maxSuccessAHT прописана в контексте base.html и тянется с БД
            if (valueAHT <= maxSuccessAHT) {
                daylyAHT.classList.add("success");
            }
            else {
                daylyAHT.classList.add("danger");
            }
        }
        let weeklyAHT = module.querySelector(".weekly_aht *")
        if (weeklyAHT != null) {
            let valueAHT= parsingInt(weeklyAHT.textContent);
			// maxSuccessAHT прописана в контексте base.html и тянется с БД
            if (valueAHT <= maxSuccessAHT) {
                weeklyAHT.classList.add("success");
            }
            else {
                weeklyAHT.classList.add("danger");
            }
        }
        let mountlyAHT = module.querySelector(".mountly_aht *")
        if (mountlyAHT != null) {
            let valueAHT= parsingInt(mountlyAHT.textContent);
			// maxSuccessAHT прописана в контексте base.html и тянется с БД
            if (valueAHT <= maxSuccessAHT) {
                mountlyAHT.classList.add("success");
            }
            else {
                mountlyAHT.classList.add("danger");
            }
        }
        let numWorkedAfterDeadline = module.querySelector(".num_worked_after_deadline *")
        if (numWorkedAfterDeadline != null) {
            let valueWorkedAfterDeadline= +numWorkedAfterDeadline.textContent;
            if (valueWorkedAfterDeadline > 0) {
                numWorkedAfterDeadline.classList.add("danger");
            }
        }
    });
};

function changeAnlyticsValue(data) {
    console.log(data)
    let analyticsSl = [[document.querySelector(".sl-first-line"),data.dashboard_data.sl.first_line, data.dashboard_data.analytics.sl.first_line],
                       [document.querySelector(".sl-vip-line"), data.dashboard_data.sl.vip_line, data.dashboard_data.analytics.sl.vip_line],
                       [document.querySelector(".sl-general"), data.dashboard_data.sl.general, data.dashboard_data.analytics.sl.general]]

    analyticsSl.forEach(function setAnalyticsSlParam(Obj) {
        Obj[0].querySelector(".dayly_sl *").textContent = Obj[1].dayly_sl + '%'
        Obj[0].querySelector(".weekly_sl *").textContent = Obj[1].weekly_sl + '%'
        Obj[0].querySelector(".mountly_sl *").textContent = Obj[1].mountly_sl + '%'
        Obj[0].querySelector(".num_issues *").textContent = Obj[1].num_issues
        Obj[0].querySelector(".num_worked_before_deadline *").textContent = Obj[1].num_worked_before_deadline
    });

    let analyticsMttr = document.querySelector(".mttr");
    analyticsMttr.querySelector(".dayly_mttr *").textContent = data.dashboard_data.mttr.average_mttr_tech_support + ' мин.'
    analyticsMttr.querySelector(".weekly_mttr *").textContent = data.dashboard_data.mttr.weekly_average_mttr_tech_support + ' мин.'
    analyticsMttr.querySelector(".mountly_mttr *").textContent = data.dashboard_data.mttr.mountly_average_mttr_tech_support + ' мин.'
    analyticsMttr.querySelector(".num_issues *").textContent = data.dashboard_data.mttr.num_issues

    let analyticsFlr = document.querySelector(".flr");
    analyticsFlr.querySelector(".dayly_flr *").textContent = data.dashboard_data.flr.level + '%'
    analyticsFlr.querySelector(".weekly_flr *").textContent = data.dashboard_data.flr.weekly_level + '%'
    analyticsFlr.querySelector(".mountly_flr *").textContent = data.dashboard_data.flr.mountly_level + '%'
    analyticsFlr.querySelector(".num_primary_issues *").textContent = data.dashboard_data.flr.num_primary_issues
    analyticsFlr.querySelector(".num_issues_closed_independently *").textContent = data.dashboard_data.flr.num_issues_closed_independently    

    let analyticsAht = document.querySelector(".aht");
    analyticsAht.querySelector(".dayly_aht *").textContent = data.dashboard_data.aht.dayly_aht + ' мин.'
    analyticsAht.querySelector(".weekly_aht *").textContent = data.dashboard_data.aht.weekly_aht + ' мин.'
    analyticsAht.querySelector(".mountly_aht *").textContent = data.dashboard_data.aht.mountly_aht + ' мин.'
    analyticsAht.querySelector(".issues_received *").textContent = data.dashboard_data.aht.issues_received
    changeAnalytics();
};
function createNotification(){
    let updatesCollectionElem = document.querySelector('#raw-notifications');
    let updatesCollection = JSON.parse(updatesCollectionElem.textContent);
    updatesCollection = updatesCollection.reverse()
    updatesCollection.forEach(function(notification){
        notification.fields.issue = JSON.parse(notification.fields.issue)
        createNotify(notification.fields, document.querySelector('.updates'))
    });
    updatesCollectionElem.remove();
};

changeAnalytics();
createNotification();