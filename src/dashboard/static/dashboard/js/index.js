const cardDailySl = document.querySelector(".daily-sl");
const cardWeeklySl = document.querySelector(".weekly-sl");
const cardMonthlySl = document.querySelector(".monthly-sl");
const cardDailySlVip = document.querySelector(".daily-sl-vip");
const cardWeeklySlVip = document.querySelector(".weekly-sl-vip");
const cardMonthlySlVip = document.querySelector(".monthly-sl-vip");
const cardDailyFlr = document.querySelector(".daily-flr");
const cardDailyMttr = document.querySelector(".daily-mttr");
const options = {year: 'numeric', month: 'numeric', day: 'numeric',
                 timezone: 'Moscow'};

function month_name(dt){
    mlist = [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ];
    return mlist[dt.getMonth()];
};

function formatWeekDataString(dateFirst, dateSecond) {
    dateFirst = new Date(dateFirst)
    dateSecond = new Date(dateSecond)
    let monthFirstDate = String(dateFirst.getMonth() + 1).length === 1 ? '0' + String(dateFirst.getMonth() + 1): String(dateFirst.getMonth() + 1);
    let monthSecondDate = String(dateSecond.getMonth() + 1).length === 1 ? '0' + String(dateSecond.getMonth() + 1): String(dateSecond.getMonth() + 1);
    let firstPath = dateFirst.getDate() + '.' + monthFirstDate
    let secondPath = dateSecond.getDate() + '.' + monthSecondDate
    return firstPath + ' - ' + secondPath
}

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

function changeDayValue(data) {
    console.log(data)
    // first line
    counterDailySlFirstLine = cardDailySl.querySelector(".number *");
    date = cardDailySl.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options)
    counterDailySlFirstLine.textContent = data.dashboard_data.sl.first_line.dayly_sl;
    counterWeeklySlFirstLine = cardWeeklySl.querySelector(".number *");
    date = cardWeeklySl.querySelector(".middle h1");
    date.textContent = formatWeekDataString(data.dates.monday_this_week, data.dates.sunday_this_week)
    counterWeeklySlFirstLine.textContent = data.dashboard_data.sl.first_line.weekly_sl;  
    counterMonthlySlFirstLine = cardMonthlySl.querySelector(".number *");
    date = cardMonthlySl.querySelector(".middle h1");
    date.textContent = month_name(new Date(data.dates.chosen_date));    
    counterMonthlySlFirstLine.textContent = data.dashboard_data.sl.first_line.mountly_sl;
    // vip line
    counterDailySlVipLine = cardDailySlVip.querySelector(".number *");
    date = cardDailySlVip.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options)    
    counterDailySlVipLine.textContent = data.dashboard_data.sl.vip_line.dayly_sl;
    counterWeeklySlVipLine = cardWeeklySlVip.querySelector(".number *");
    date = cardWeeklySlVip.querySelector(".middle h1");
    date.textContent = formatWeekDataString(data.dates.monday_this_week, data.dates.sunday_this_week)    
    counterWeeklySlVipLine.textContent = data.dashboard_data.sl.vip_line.weekly_sl; 
    counterMonthlySlVipLine = cardMonthlySlVip.querySelector(".number *");
    date = cardMonthlySlVip.querySelector(".middle h1");
    date.textContent = month_name(new Date(data.dates.chosen_date));    
    counterMonthlySlVipLine.textContent = data.dashboard_data.sl.vip_line.mountly_sl;
    // mttr
    counterDailyMttr = cardDailyMttr.querySelector(".number *");
    date = cardDailyMttr.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options)
    counterDailyMttr.textContent = data.dashboard_data.mttr.average_mttr_tech_support;
    // flr
    counterDailyFlr = cardDailyFlr.querySelector(".number *");
    date = cardDailyFlr.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options)
    counterDailyFlr.textContent = data.dashboard_data.flr.level;
    changeCardProgress();
    changeAnalytics();
}

function getDashboardData() {
    let current_date = document.getElementById('date').value;
    $.post('/json/dashboard', { date: current_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
        changeDayValue(data)
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

