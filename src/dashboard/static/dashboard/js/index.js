


let current_date = getTodayDate();



function getTodayDate() {
    var d = new Date();
    var day = d.getDate()
    var month = d.getMonth() + 1 
    var year = d.getFullYear()
    if (day < 10) {
        day = '' + 0 + day;
    }
    if (month < 10) {
        month = '' + 0 + month;
    }
    var today_date = year + "-" + month + "-" + day;
    return today_date
    }


// set today in calend
document.addEventListener('DOMContentLoaded', function () {
    var name_input = document.getElementById('date')
    name_input.value = current_date;
});

function setProgress(percent, progressCircle) {
    const progress_circle = cart.querySelector("#circle")
    const offset = circumference - percent / 100 * circumference;
    progressCircle.style.strokeDashoffset = offset;
    var a = 1;
    var run = setInterval(frames, 10);
    function frames() {
        a = a + 1;
        if (a - 1 == percent) {
            clearInterval(run);
        } else {
            var counter = document.querySelector(".number h3");
            counter.textContent = a + "%";
        }
    }

}


function setCardProgress(num, card, cardtext, warningstatus, unit) {
    if (num < 0) {
        var num = 0
    } else if (num > 100) {
        var num = 100
    }

    var progressCircle = card.querySelector(".circle");
    var radius = progressCircle.r.baseVal.value;
    var circumference = 2 * Math.PI * radius;

    var offset = circumference - num / 100 * circumference;
    progressCircle.style.strokeDashoffset = offset;

    if (warningstatus == true) {
        card.classList.add("warning-dash")
    } else {
        card.classList.remove("warning-dash")
    }

    var date = card.querySelector(".middle h1");
    date.textContent = cardtext;
    var a = -1;
    var run = setInterval(frames, 10);
    function frames() {
        if (a == num) {
            clearInterval(run);
        }
        var counter = card.querySelector(".number *");
        counter.textContent = a + unit;
        a = a + 1;
    }
}


function updateCardProgress() {
    $.post('/json/dashboard', { date: current_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
        var cardDailySl = document.querySelector(".daily-sl");
        var cardWeeklySl = document.querySelector(".weekly-sl");
        var cardMonthlySl = document.querySelector(".monthly-sl");
        var cardDailySlVip = document.querySelector(".daily-sl-vip");
        var cardWeeklySlVip = document.querySelector(".weekly-sl-vip");
        var cardMonthlySlVip = document.querySelector(".monthly-sl-vip");
        var cardDailyFlr = document.querySelector(".daily-flr");
        var cardDailyMttr = document.querySelector(".daily-mttr");
        setCardProgress(data.DayServiceLevelFirstLine, cardDailySl, data.Today, false, '%');
        setCardProgress(data.WeeklyServiceLevelFirstLine, cardWeeklySl, data.Week,  false, '%');
        setCardProgress(data.MonthlyServiceLevelFirstLine, cardMonthlySl, data.NameMonth,  false, '%');
        setCardProgress(data.DayServiceLevelVipLine, cardDailySlVip, data.Today, false, '%');
        setCardProgress(data.WeeklyServiceLevelVipLine, cardWeeklySlVip, data.Week, false, '%');
        setCardProgress(data.MonthlyServiceLevelVipLine, cardMonthlySlVip, data.NameMonth, false, '%');
        setCardProgress(data.DayFlr, cardDailyFlr, data.Today, false, '%');
        setCardProgress(data.DayMttr, cardDailyMttr, data.Today, false, 'м.');
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

