const alarmValueSL = 80


function setProgress(percent, progressCircle) {
    let progress_circle = cart.querySelector("#circle")
    let offset = circumference - percent / 100 * circumference;
    progressCircle.style.strokeDashoffset = offset;
    let a = 1;
    let run = setInterval(frames, 10);
    function frames() {
        a = a + 1;
        if (a - 1 == percent) {
            clearInterval(run);
        } else {
            let counter = document.querySelector(".number h3");
            counter.textContent = a + "%";
        }
    }

}

// function setCardProgress(num, card, cardtext, warningstatus, unit) {
//     if (num < 0) {
//         let num = 0
//     } else if (num > 100) {
//         let num = 100
//     }

//     let progressCircle = card.querySelector(".circle");
//     let radius = progressCircle.r.baseVal.value;
//     let circumference = 2 * Math.PI * radius;

//     let offset = circumference - num / 100 * circumference;
//     progressCircle.style.strokeDashoffset = offset;

//     if (warningstatus == true) {
//         card.classList.add("warning-dash")
//     } else {
//         card.classList.remove("warning-dash")
//     }

//     let date = card.querySelector(".middle h1");
//     date.textContent = cardtext;
//     let a = -1;
//     let run = setInterval(frames, 10);
//     function frames() {
//         if (a == num) {
//             clearInterval(run);
//         }
//         let counter = card.querySelector(".number *");
//         counter.textContent = a + unit;
//         a = a + 1;
//     }
// }

function setCardProgress(card, unit) {
    let counter = card.querySelector(".number *");
    let value = +counter.textContent
    let progressCircle = card.querySelector(".circle");

    let radius = progressCircle.r.baseVal.value;
    let circumference = 2 * Math.PI * radius;
    let offset = circumference - value / 100 * circumference;
    progressCircle.style.strokeDashoffset = offset;

    counter.textContent = 0
    let a = -1;
    let run = setInterval(frames, 10);
    function frames() {
        if (a == value) {
            clearInterval(run);
        }
        counter.textContent = a + unit;
        a = a + 1;
    }
}

function parsingInt(textString) {
    return parseInt(textString.replace(/^(0$|-?[1-9]\d*(\.\d*[1-9]$)?|-?0\.\d*[1-9])$/, ''));
}


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
                ratingObj.classList.add("warning");
            } else if (valueRating < 0){
                ratingObj.textContent = "< на " + Math.abs(valueRating) + "%";
                ratingObj.classList.add("success");
            }
            else {
                //pass
            }
        });
        let daylySL = module.querySelector(".dayly_sl *")
        let valueSL= parsingInt(daylySL.textContent);
        if (valueSL >= alarmValueSL) {
            daylySL.classList.add("success");
        }
        else {
            daylySL.classList.add("warning");
        }
    });
}

function changeCardProgress() {
    let cardDailySl = document.querySelector(".daily-sl");
    let cardWeeklySl = document.querySelector(".weekly-sl");
    let cardMonthlySl = document.querySelector(".monthly-sl");
    let cardDailySlVip = document.querySelector(".daily-sl-vip");
    let cardWeeklySlVip = document.querySelector(".weekly-sl-vip");
    let cardMonthlySlVip = document.querySelector(".monthly-sl-vip");
    let cardDailyFlr = document.querySelector(".daily-flr");
    let cardDailyMttr = document.querySelector(".daily-mttr");
    setCardProgress(cardDailySl, '%')
    setCardProgress(cardWeeklySl, '%')
    setCardProgress(cardMonthlySl, '%')
    setCardProgress(cardDailySlVip, '%')
    setCardProgress(cardWeeklySlVip, '%')
    setCardProgress(cardMonthlySlVip, '%')
    setCardProgress(cardDailyFlr, '%')
    setCardProgress(cardDailyMttr, ' м.')    
}

function getDashboardData() {
    let current_date = document.getElementById('date').value;
    $.post('/json/dashboard', { date: current_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
        console.log(data)
    });
}


$(document).ready(function(){
    changeCardProgress();
    changeAnalytics();
    setInterval('updateCardProgress()', 600000);
});

$("#form-date").submit(function(event) {
    event.preventDefault();
    getDashboardData();
});

