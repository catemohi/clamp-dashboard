const cardDailySl = document.querySelector(".daily-sl");
const cardWeeklySl = document.querySelector(".weekly-sl");
const cardMonthlySl = document.querySelector(".monthly-sl");
const cardDailySlVip = document.querySelector(".daily-sl-vip");
const cardWeeklySlVip = document.querySelector(".weekly-sl-vip");
const cardMonthlySlVip = document.querySelector(".monthly-sl-vip");
const cardDailyFlr = document.querySelector(".daily-flr");
const cardDailyMttr = document.querySelector(".daily-mttr");
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

// function setCardProgress(num, card, cardtext, dangerstatus, unit) {
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

//     if (dangerstatus == true) {
//         card.classList.add("danger-dash")
//     } else {
//         card.classList.remove("danger-dash")
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

function changeCardProgress() {
    setCardProgress(cardDailySl, '%')
    setCardProgress(cardWeeklySl, '%')
    setCardProgress(cardMonthlySl, '%')
    setCardProgress(cardDailySlVip, '%')
    setCardProgress(cardWeeklySlVip, '%')
    setCardProgress(cardMonthlySlVip, '%')
    setCardProgress(cardDailyFlr, '%')
    setCardProgress(cardDailyMttr, ' м.')    
}

async function  getPostDashboardData() {
    let post_data = {
        date: document.getElementById('date').value,
        csrfmiddlewaretoken: window.CSRF_TOKEN};
    
    let response = await fetch('/json/dashboard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(post_data)
    });
    let result = await response.json();
    console(result);
}


$(document).ready(function(){
    changeCardProgress();
    changeAnalytics();
    setInterval('updateCardProgress()', 600000);
});

$("#form-date").submit(function(event) {
    event.preventDefault();
    getPostDashboardData();
});

