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

function setCardProgress(num, card, cardtext, warningstatus, unit) {
    if (num < 0) {
        let num = 0
    } else if (num > 100) {
        let num = 100
    }

    let progressCircle = card.querySelector(".circle");
    let radius = progressCircle.r.baseVal.value;
    let circumference = 2 * Math.PI * radius;

    let offset = circumference - num / 100 * circumference;
    progressCircle.style.strokeDashoffset = offset;

    if (warningstatus == true) {
        card.classList.add("warning-dash")
    } else {
        card.classList.remove("warning-dash")
    }

    let date = card.querySelector(".middle h1");
    date.textContent = cardtext;
    let a = -1;
    let run = setInterval(frames, 10);
    function frames() {
        if (a == num) {
            clearInterval(run);
        }
        let counter = card.querySelector(".number *");
        counter.textContent = a + unit;
        a = a + 1;
    }
}


function updateCardProgress() {
    $.post('/json/dashboard', { date: current_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
        let cardDailySl = document.querySelector(".daily-sl");
        let cardWeeklySl = document.querySelector(".weekly-sl");
        let cardMonthlySl = document.querySelector(".monthly-sl");
        let cardDailySlVip = document.querySelector(".daily-sl-vip");
        let cardWeeklySlVip = document.querySelector(".weekly-sl-vip");
        let cardMonthlySlVip = document.querySelector(".monthly-sl-vip");
        let cardDailyFlr = document.querySelector(".daily-flr");
        let cardDailyMttr = document.querySelector(".daily-mttr");
        console.log(data)
        // setCardProgress(data.DayServiceLevelFirstLine, cardDailySl, data.Today, false, '%');
        // setCardProgress(data.WeeklyServiceLevelFirstLine, cardWeeklySl, data.Week,  false, '%');
        // setCardProgress(data.MonthlyServiceLevelFirstLine, cardMonthlySl, data.NameMonth,  false, '%');
        // setCardProgress(data.DayServiceLevelVipLine, cardDailySlVip, data.Today, false, '%');
        // setCardProgress(data.WeeklyServiceLevelVipLine, cardWeeklySlVip, data.Week, false, '%');
        // setCardProgress(data.MonthlyServiceLevelVipLine, cardMonthlySlVip, data.NameMonth, false, '%');
        // setCardProgress(data.DayFlr, cardDailyFlr, data.Today, false, '%');
        // setCardProgress(data.DayMttr, cardDailyMttr, data.Today, false, 'м.');
    });
}


$(document).ready(function(){
    updateCardProgress();
    setInterval('updateCardProgress()', 600000);
});

$("#form-date").submit(function(e) {
    e.preventDefault();
    current_date = document.getElementById('date').value;
    updateCardProgress();
});

