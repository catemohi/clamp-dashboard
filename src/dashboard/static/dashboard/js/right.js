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

	let text = document.createElement('p');
	let name_hendler = document.createElement('b');
	text.innerText = notify.text;
	let time = document.createElement('small');
	time.className = "text-muted";
	time.innerText = notify.time;

	message.appendChild(text);
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
    analyticsMttr.querySelector(".average_mttr_tech_support *").textContent = data.dashboard_data.mttr.average_mttr_tech_support + 'мин.'
    analyticsMttr.querySelector(".num_issues *").textContent = data.dashboard_data.mttr.num_issues
    analyticsMttr.querySelector(".rating_to_nominal *").textContent =  data.dashboard_data.analytics.mttr.rating_to_nominal + '%'
    analyticsMttr.querySelector(".rating_to_comparison *").textContent = data.dashboard_data.analytics.mttr.rating_to_comparison + '%'

    let analyticsFlr = document.querySelector(".flr");
    analyticsFlr.querySelector(".level *").textContent = data.dashboard_data.flr.level + '%'
    analyticsFlr.querySelector(".num_primary_issues *").textContent = data.dashboard_data.flr.num_primary_issues
    analyticsFlr.querySelector(".num_issues_closed_independently *").textContent = data.dashboard_data.flr.num_issues_closed_independently    
    analyticsFlr.querySelector(".rating_to_nominal *").textContent =  data.dashboard_data.analytics.flr.rating_to_nominal + '%'
    analyticsFlr.querySelector(".rating_to_comparison *").textContent = data.dashboard_data.analytics.flr.rating_to_comparison + '%'
    changeAnalytics();
}

changeAnalytics();
