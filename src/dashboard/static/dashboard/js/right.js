// changet heme
const themeToggler = document.querySelector(".theme-toggler");
const menuBtn = document.querySelector(".menu-btn");

themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-var');

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
    
    if (themeToggler.querySelector('span:nth-child(2)').classList.contains('active')) {
        document.cookie = "theme=dark; path=/;";
        let calendarIcon = document.querySelectorAll('input[type="date"]');
        calendarIcon.forEach(function(item) {
            item.classList.toggle('invert-color')
        });
    } else {
        document.cookie = "theme=white; path=/;";
        let calendarIcon = document.querySelectorAll('input[type="date"]');
        calendarIcon.forEach(function(item) {
            item.classList.toggle('invert-color')
        });
    }

})

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
                     document.querySelector(".flr")];


    Analytics.forEach(function modifyPercentRatings(module) {
        let RatingObjs =  [module.querySelector(".rating_to_nominal *"),
                           module.querySelector(".rating_to_comparison *")];

        RatingObjs.forEach(function modifyRating(ratingObj) {
            let valueRating = parsingInt(ratingObj.textContent);
            if (valueRating > 0) {
                ratingObj.textContent = "> на " + Math.abs(valueRating) + "%";
                ratingObj.classList.add("danger");
            } else if (valueRating < 0){
                ratingObj.textContent = "< на " + Math.abs(valueRating) + "%";
                ratingObj.classList.add("success");
            }
            else {
                //pass
            }
        });

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
    let analyticsSl = [[document.querySelector(".sl-first-line"),data.dashboard_data.sl.first_line, data.dashboard_data.analytics.sl.first_line],
                       [document.querySelector(".sl-vip-line"), data.dashboard_data.sl.vip_line, data.dashboard_data.analytics.sl.vip_line],
                       [document.querySelector(".sl-general"), data.dashboard_data.sl.general, data.dashboard_data.analytics.sl.general]]

    analyticsSl.forEach(function setAnalyticsSlParam(Obj) {
        Obj[0].querySelector(".dayly_sl *").textContent = Obj[1].dayly_sl + '%'
        Obj[0].querySelector(".num_issues *").textContent = Obj[1].num_issues
        Obj[0].querySelector(".num_worked_before_deadline *").textContent = Obj[1].num_worked_before_deadline
        Obj[0].querySelector(".num_worked_after_deadline *").textContent = Obj[1].num_worked_after_deadline
        Obj[0].querySelector(".rating_to_nominal *").textContent = Obj[2].rating_to_nominal + '%'
        Obj[0].querySelector(".rating_to_comparison *").textContent = Obj[2].rating_to_comparison + '%'
    });

    let analyticsMttr = document.querySelector(".mttr");
    analyticsMttr.querySelector(".dayly_mttr *").textContent = data.dashboard_data.mttr.average_mttr_tech_support + 'мин.'
    analyticsMttr.querySelector(".num_issues *").textContent = data.dashboard_data.mttr.num_issues
    analyticsMttr.querySelector(".rating_to_nominal *").textContent =  data.dashboard_data.analytics.mttr.rating_to_nominal + '%'
    analyticsMttr.querySelector(".rating_to_comparison *").textContent = data.dashboard_data.analytics.mttr.rating_to_comparison + '%'

    let analyticsFlr = document.querySelector(".flr");
    analyticsFlr.querySelector(".dayly_flr *").textContent = data.dashboard_data.flr.level + '%'
    analyticsFlr.querySelector(".num_primary_issues *").textContent = data.dashboard_data.flr.num_primary_issues
    analyticsFlr.querySelector(".num_issues_closed_independently *").textContent = data.dashboard_data.flr.num_issues_closed_independently    
    analyticsFlr.querySelector(".rating_to_nominal *").textContent =  data.dashboard_data.analytics.flr.rating_to_nominal + '%'
    analyticsFlr.querySelector(".rating_to_comparison *").textContent = data.dashboard_data.analytics.flr.rating_to_comparison + '%'
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