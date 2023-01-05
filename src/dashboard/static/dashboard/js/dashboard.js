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
    mlist = [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
              "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ];
    return mlist[dt.getMonth()];
};

function formatWeekDataString(dateFirst, dateSecond) {
    dateFirst = new Date(dateFirst)
    dateSecond = new Date(dateSecond)
    let monthFirstDate = String(dateFirst.getMonth() + 1).length === 1 
        ? '0' + (dateFirst.getMonth() + 1): String(dateFirst.getMonth() + 1);
    let monthSecondDate = String(dateSecond.getMonth() + 1).length === 1 
        ? '0' + (dateSecond.getMonth() + 1): String(dateSecond.getMonth() + 1);
    let dayFirstDate = String(dateFirst.getDate()).length === 1 
        ? '0' + (dateFirst.getDate()): String(dateFirst.getDate());
    let daySecondDate = String(dateSecond.getDate()).length === 1 
        ? '0' + (dateSecond.getDate()): String(dateSecond.getDate());

    let firstPath = dayFirstDate + '.' + monthFirstDate;
    let secondPath = daySecondDate + '.' + monthSecondDate;
    return firstPath + ' - ' + secondPath;
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

function changeProgresTabsValue(data) {
    let current_date = document.getElementById('date')
    current_date.value = new Date(data.dates.chosen_date)
    // first line
    counterDailySlFirstLine = cardDailySl.querySelector(".number *");
    date = cardDailySl.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options);
    counterDailySlFirstLine.textContent = data.dashboard_data.sl.first_line.dayly_sl;
    counterWeeklySlFirstLine = cardWeeklySl.querySelector(".number *");
    date = cardWeeklySl.querySelector(".middle h1");
    date.textContent = formatWeekDataString(
        data.dates.monday_this_week, data.dates.sunday_this_week)
    counterWeeklySlFirstLine.textContent = data.dashboard_data.sl.first_line.weekly_sl;  
    counterMonthlySlFirstLine = cardMonthlySl.querySelector(".number *");
    date = cardMonthlySl.querySelector(".middle h1");
    date.textContent = month_name(new Date(data.dates.chosen_date));    
    counterMonthlySlFirstLine.textContent = data.dashboard_data.sl.first_line.mountly_sl;
    // vip line
    counterDailySlVipLine = cardDailySlVip.querySelector(".number *");
    date = cardDailySlVip.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options);    
    counterDailySlVipLine.textContent = data.dashboard_data.sl.vip_line.dayly_sl;
    counterWeeklySlVipLine = cardWeeklySlVip.querySelector(".number *");
    date = cardWeeklySlVip.querySelector(".middle h1");
    date.textContent = formatWeekDataString(data.dates.monday_this_week, data.dates.sunday_this_week);
    counterWeeklySlVipLine.textContent = data.dashboard_data.sl.vip_line.weekly_sl; 
    counterMonthlySlVipLine = cardMonthlySlVip.querySelector(".number *");
    date = cardMonthlySlVip.querySelector(".middle h1");
    date.textContent = month_name(new Date(data.dates.chosen_date));    
    counterMonthlySlVipLine.textContent = data.dashboard_data.sl.vip_line.mountly_sl;
    // mttr
    counterDailyMttr = cardDailyMttr.querySelector(".number *");
    date = cardDailyMttr.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options);
    counterDailyMttr.textContent = data.dashboard_data.mttr.average_mttr_tech_support;
    // flr
    counterDailyFlr = cardDailyFlr.querySelector(".number *");
    date = cardDailyFlr.querySelector(".middle h1");
    date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options);
    counterDailyFlr.textContent = data.dashboard_data.flr.level;
    changeCardProgress();
}

function getDashboardData() {
    let current_date = document.getElementById('date').value;
    if (new Date(current_date) > new Date(Date.now())) {
        alert("Выбрана недопустимая дата!");
        return
    }
    $.post('/json/dashboard', { date: current_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
        changeProgresTabsValue(data)
    });
}

$(document).ready(function(){
    changeCardProgress();
});

$("#form-date").submit(function(event) {
    event.preventDefault();
    getDashboardData();
});

