const allCard  = document.querySelectorAll(".card");
const cardDailySl = document.querySelector(".daily-sl");
const cardWeeklySl = document.querySelector(".weekly-sl");
const cardMonthlySl = document.querySelector(".monthly-sl");
const cardDailySlVip = document.querySelector(".daily-sl-vip");
const cardWeeklySlVip = document.querySelector(".weekly-sl-vip");
const cardMonthlySlVip = document.querySelector(".monthly-sl-vip");
const cardDailyFlr = document.querySelector(".daily-flr");
const cardWeeklyFlr = document.querySelector(".weekly-flr");
const cardMountlyFlr = document.querySelector(".mountly-flr");
const cardDailyMttr = document.querySelector(".daily-mttr");
const cardWeeklyMttr = document.querySelector(".weekly-mttr");
const cardMountlyMttr = document.querySelector(".mountly-mttr");
const cardDailyAht = document.querySelector(".daily-aht");
const cardWeeklyAht = document.querySelector(".weekly-aht");
const cardMountlyAht = document.querySelector(".mountly-aht");
const options_dash = {year: 'numeric', month: 'numeric', day: 'numeric',
                      timezone: 'Moscow'};

function month_name(dt){
  mlist = [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
            "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ];
  return mlist[dt.getMonth()];
};

document.querySelector('.filter').addEventListener('click', (event) => {
  // Анонимная функция для фильтрации отоброжаемых карточек
  if (event.target.tagName !== "LI") {
    return false
  };
  let filterClass = event.target.dataset["f"];
  allCard.forEach( (element) => {
    element.classList.remove('hide-card');
    element.classList.remove('active-filter');
    if (!element.classList.contains(filterClass) && filterClass !== 'all') {
      element.classList.add('hide-card');
      element.classList.add('active-filter');
    };
  });
});

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
};

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
    };
  };
};

function setCardProgress(card, typeReport, unit) {
  let counter = card.querySelector(".number *");
  let value = +counter.textContent;
  let progressCircle = card.querySelector(".circle");
  let radius = progressCircle.r.baseVal.value;
  let circumference = 2 * Math.PI * radius;
  let offset = circumference - value / 100 * circumference;
  progressCircle.style.strokeDashoffset = offset;
  counter.textContent = 0;
  let a = -1;
  let run = setInterval(frames, 10);
  function frames() {
    if (a == value) {
        clearInterval(run);
    };
    counter.textContent = a + unit;
    a = a + 1;
  };
  switch(typeReport) {
    case 'sl':
      if (value < minSuccessSL) {
        card.querySelector(".number").classList.add("danger");
      } else {
        card.querySelector(".number").classList.remove("danger");
      };
      break;
    
    case 'mttr':
      if (value > maxSuccessMTTR) {
          card.querySelector(".number").classList.add("danger");
      } else {
          card.querySelector(".number").classList.remove("danger");
      };
      break;
    
    case 'flr':
      if (value < minSuccessFLR) {
        card.querySelector(".number").classList.add("danger");
      } else {
        card.querySelector(".number").classList.remove("danger");
      };
      break;

    case 'aht':
      if (value < maxSuccessAHT) {
        card.querySelector(".number").classList.add("danger");
      } else {
        card.querySelector(".number").classList.remove("danger");
      };
      break;
      
    default:
      // pass
      break;
  };
};

function changeCardProgress() {
  setCardProgress(cardDailySl, 'sl', '%');
  setCardProgress(cardWeeklySl, 'sl', '%');
  setCardProgress(cardMonthlySl, 'sl', '%');
  setCardProgress(cardDailySlVip, 'sl', '%');
  setCardProgress(cardWeeklySlVip, 'sl', '%');
  setCardProgress(cardMonthlySlVip, 'sl', '%');
  setCardProgress(cardDailyFlr, 'flr', '%');
  setCardProgress(cardWeeklyFlr, 'flr', '%');
  setCardProgress(cardMountlyFlr, 'flr', '%');
  setCardProgress(cardDailyMttr, 'mttr', ' м.');
  setCardProgress(cardWeeklyMttr, 'mttr', ' м.');
  setCardProgress(cardMountlyMttr, 'mttr', ' м.');
  setCardProgress(cardDailyAht, 'aht', ' м.');
  setCardProgress(cardWeeklyAht, 'aht', ' м.');
  setCardProgress(cardMountlyAht, 'aht', ' м.');
};

function changeProgresTabsValue(data) {
  console.log(data);
  let current_date = document.getElementById('date');
  current_date.value = data.dates.chosen_date;
  // first line
  counterDailySlFirstLine = cardDailySl.querySelector(".number *");
  date = cardDailySl.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
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
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);    
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
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterDailyMttr.textContent = data.dashboard_data.mttr.average_mttr_tech_support;

  counterWeeklyMttr = cardWeeklyMttr.querySelector(".number *");
  date = cardWeeklyMttr.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterWeeklyMttr.textContent = data.dashboard_data.mttr.weekly_average_mttr_tech_support;

  counterMountlyMttr = cardMountlyMttr.querySelector(".number *");
  date = cardMountlyMttr.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterMountlyMttr.textContent = data.dashboard_data.mttr.mountly_average_mttr_tech_support;
  // flr
  counterDailyFlr = cardDailyFlr.querySelector(".number *");
  date = cardDailyFlr.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterDailyFlr.textContent = data.dashboard_data.flr.level;

  counterWeeklyFlr = cardWeeklyFlr.querySelector(".number *");
  date = cardWeeklyFlr.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterWeeklyFlr.textContent = data.dashboard_data.flr.weekly_level;

  counterMountlyFlr = cardMountlyFlr.querySelector(".number *");
  date = cardMountlyFlr.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterMountlyFlr.textContent = data.dashboard_data.flr.mountly_level;
  // aht
  counterDailyAht = cardDailyAht.querySelector(".number *");
  date = cardDailyAht.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterDailyAht.textContent = data.dashboard_data.aht.dayly_aht;

  counterWeeklyAht = cardWeeklyAht.querySelector(".number *");
  date = cardWeeklyAht.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterDailyAht.textContent = data.dashboard_data.aht.weekly_aht;

  counterMountlyAht = cardMountlyAht.querySelector(".number *");
  date = cardMountlyAht.querySelector(".middle h1");
  date.textContent = new Date(data.dates.chosen_date).toLocaleString("ru", options_dash);
  counterMountlyAht.textContent = data.dashboard_data.aht.mountly_aht;
  changeCardProgress();
};

function getDashboardData() {
  let current_date = document.getElementById('date').value;
  if (new Date(current_date) > new Date(Date.now())) {
    alert("Выбрана недопустимая дата!");
    return
  }
  $.post('/json/dashboard', { date: current_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
    changeProgresTabsValue(data);
    changeAnlyticsValue(data);
  });
};

$(document).ready(function(){
  changeCardProgress();
});

$("#form-date").submit(function(event) {
  document.body.style.cursor = 'progress';
  event.preventDefault();
  getDashboardData();
  document.body.style.cursor = 'default';
});
