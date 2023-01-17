
function getDateReports() {
  return [ document.getElementById('date-desired').value,
           document.getElementById('date-comparison').value ];
};

function reloadDatatable( desiredDate, comparisonDate ) {
  let responce = $.post( '/json/reports', { desired_date: desiredDate,
                                            comparison_date: comparisonDate,
                                            csrfmiddlewaretoken: window.CSRF_TOKEN } );
  responce.done(function ( data ) {
    console.log(data)
    let dataSet = [
      [ 1, 'Дата', desiredDate, comparisonDate ],
      [ 2, 'Количество обращений за день на первую линию',
        data.desired_date.sl.first_line.num_issues,
        data.comparison_date.sl.first_line.num_issues ],
      [ 3, 'Количество обращений первой линии принятых вовремя',
        data.desired_date.sl.first_line.num_worked_before_deadline,
        data.comparison_date.sl.first_line.num_worked_before_deadline ],
      [ 4, 'Количество обращений первой линии принятых после срока',
        data.desired_date.sl.first_line.num_worked_after_deadline,
        data.comparison_date.sl.first_line.num_worked_after_deadline ],
      [ 5, 'Нагрузка первой линии относительно нормы',
        data.desired_date.analytics.sl.first_line.rating_to_nominal, '-' ],
      [ 6, 'Нагрузка первой линии относительно дня сравнения',
        data.desired_date.analytics.sl.first_line.rating_to_comparison, '-' ],
      [ 7, 'Service Level первой линии',
        data.desired_date.sl.first_line.dayly_sl,
        data.comparison_date.sl.first_line.dayly_sl ],
      [ 8, 'Количество обращений за день на VIP линию',
        data.desired_date.sl.vip_line.num_issues,
        data.comparison_date.sl.vip_line.num_issues ],
      [ 9, 'Количество обращений VIP линии принятых вовремя',
        data.desired_date.sl.vip_line.num_worked_before_deadline,
        data.comparison_date.sl.vip_line.num_worked_before_deadline ],
      [ 10, 'Количество обращений VIP линии принятых после срока',
        data.desired_date.sl.vip_line.num_worked_after_deadline,
        data.comparison_date.sl.vip_line.num_worked_after_deadline ],
      [ 11, 'Нагрузка VIP линии относительно нормы',
        data.desired_date.analytics.sl.vip_line.rating_to_nominal,
        '-' ],
      [ 12, 'Нагрузка VIP линии относительно дня сравнения',
        data.desired_date.analytics.sl.vip_line.rating_to_comparison,
        '-' ],
      [ 13, 'Service Level VIP линии',
        data.desired_date.sl.vip_line.dayly_sl,
        data.comparison_date.sl.vip_line.dayly_sl ],
      [ 14, 'Общее количество обращений за день',
        data.desired_date.sl.general.num_issues,
        data.comparison_date.sl.general.num_issues ],
      [ 15, 'Общее количество обращений принятых вовремя',
        data.desired_date.sl.general.num_worked_before_deadline,
        data.comparison_date.sl.general.num_worked_before_deadline ],
      [ 16, 'Общее количество обращений принятых после срока',
        data.desired_date.sl.general.num_worked_after_deadline,
        data.comparison_date.sl.general.num_worked_after_deadline ],
      [ 17, 'Общая нагрузка относительно нормы',
        data.desired_date.analytics.sl.general.rating_to_nominal,
        '-' ],
      [ 18, 'Общая нагрузка относительно дня сравнения',
        data.desired_date.analytics.sl.general.rating_to_comparison,
        '-' ],
      [ 19, 'Общий Service Level',
        data.desired_date.sl.general.dayly_sl,
        data.comparison_date.sl.general.dayly_sl ],
      [ 20, 'MTTR',
        data.desired_date.mttr.average_mttr_tech_support,
        data.comparison_date.mttr.average_mttr_tech_support],
      [ 21, 'Общее количество закрытых обращений',
        data.desired_date.mttr.num_issues,
        data.comparison_date.mttr.num_issues ],
      [ 22, 'Общая нагрузка относительно нормы',
        data.desired_date.analytics.mttr.rating_to_nominal,
        '-'],
      [ 23, 'Общая нагрузка относительно дня сравнения',
        data.desired_date.analytics.mttr.rating_to_nominal,
        '-'],
      [ 24, 'FLR',
        data.desired_date.flr.level,
        data.comparison_date.flr.level],
      [ 25, 'Общее количество первичных обращений',
        data.desired_date.flr.num_primary_issues,
        data.comparison_date.flr.num_primary_issues],
      [ 26, 'Общая нагрузка относительно нормы',
        data.desired_date.analytics.flr.rating_to_nominal,
        '-'],
      [ 27, 'Общая нагрузка относительно дня сравнения',
        data.desired_date.analytics.flr.rating_to_comparison,
        '-']
      ];
      let table = $('#trouble-table').DataTable({
        data: dataSet,
        columns: [
          { title: 'Пункт' },
          { title: 'Наименование' },
          { title: 'Интересующий день' },
          { title: 'Сравнивнение' },
        ],
        autoWidth: false,
        bDestroy: true,
        bAutoWidth: false,
        bPaginate: false,
        dom: 'Bfrtip',
        buttons: [
          'csv', 'excel', 'pdf'
        ],
      });
      table.column(0).visible(false);
  });
};

$("#desired-date").submit(function(event) {
  event.preventDefault();
  let dateCollection = getDateReports();
  reloadDatatable(dateCollection[0], dateCollection[1]);
});

$("#comparison-date").submit(function(event) {
  event.preventDefault();
  let dateCollection = getDateReports();
  reloadDatatable(dateCollection[0], dateCollection[1]);
});

$(document).ready(function () {
  let dateCollection = getDateReports();
  reloadDatatable(dateCollection[0], dateCollection[1]);
});
// function getReport() {
//     var desired_date = getDate(-1)
//     var comparison_date = getDate(-2)
//     console.log(desired_date, comparison_date)
//     $.post('/json/reports', { desired_date: desired_date, comparison_date: comparison_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
//         console.log(data);
//     });
// }
// getReport()

// function getDate(offset) {
  //   var d = new Date();
  //   var day = d.getDate() + offset
  //   var month = d.getMonth() + 1 
  //   var year = d.getFullYear()
  //   if (day < 10) {
  //       day = '' + 0 + day;
  //   }
  //   if (month < 10) {
  //       month = '' + 0 + month;
  //   }
  //   var today_date = year + "-" + month + "-" + day;
  //   return today_date
  // };
  
  // $(document).ready(function () {
//   var cookies = document.cookie.split(/[;] */).reduce(function(result, pairStr) {
//       var arr = pairStr.split('=');
//       if (arr.length === 2) { result[arr[0]] = arr[1]; }
//       return result;
//   }, {});
//   var table = $('#trouble-table').DataTable({
//       "ajax": {
//           'type': 'POST',
//           'url': '/json/reports',
//           'data': function ( d ) {
//               d.csrfmiddlewaretoken = cookies["csrftoken"],
//               d.desired_date = document.getElementById('date-desired').value,
//               d.comparison_date = document.getElementById('date-comparison').value
//           },
//       },
      // dom: 'Bfrtip',
      // buttons: [
      //     'csv', 'excel', 'pdf'
      // ],
//       "columns": [
//           {"data": "number"},
//           {"data": "name"},
//           {"data": "desired_date"},
//           {"data": "comparison_date"},
//       ],
      // "autoWidth": false,
      // "bAutoWidth": false,
      // "bPaginate": false
//   });
//   table.column(0).visible(false);