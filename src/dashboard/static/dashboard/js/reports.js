
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
      [ 1, 'Дата', new Date(desiredDate).toLocaleString("ru", options), new Date(comparisonDate).toLocaleString("ru", options) ],
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
          { "title": "Пункт", "className": "column-index" },
          { "title": "Наименование", "className": "column-name" },
          { "title": "Интересующий день", "className": "desired-date" },
          { "title": "Сравнивнение", "className": "comparison-date" },
        ],
        autoWidth: false,
        bDestroy: true,
        bAutoWidth: false,
        bPaginate: false,
        dom: 'Bfrtip',
        buttons: [
          'csv', 'excel', 'pdf'
        ],
        rowCallback: function( row, data, index ) {
          console.log(data)
          if ( data[1].toLowerCase().indexOf( 'нагрузка' ) != -1 ) {
            if ( data[2] <= 0 ) {
              $( "td:eq(2)", row ).addClass( "success" );
              $( "td:eq(2)", row ).removeClass( "danger" );
              
              data[2] = 'меньше на ' + Math.abs(data[2]) + '%';
            } else {
              $( "td:eq(2)", row ).addClass( "danger" );
              $( "td:eq(2)", row ).removeClass( "success" );
              data[2] = 'больше на ' + Math.abs(data[2]) + '%';
            };
            $( "td:eq(2)", row ).addClass( "analitic" );
            $( "td:eq(2)", row ).text(data[2]);

          } else if ( data[1].toLowerCase().indexOf( 'service' ) != -1) {
            if ( data[2] >= minSuccessSL ) {
              $( "td:eq(2)", row ).addClass( "success" );
              $( "td:eq(2)", row ).removeClass( "danger" );
            } else {
              $( "td:eq(2)", row ).addClass( "danger" );
              $( "td:eq(2)", row ).removeClass( "success" );
            };
            data[2] = data[2] + '%';
            if ( data[3] >= minSuccessSL ) {
              $( "td:eq(3)", row ).addClass( "success" );
              $( "td:eq(3)", row ).removeClass( "danger" );
            } else {
              $( "td:eq(3)", row ).addClass( "danger" );
              $( "td:eq(3)", row ).removeClass( "success" );
            };
            data[3] = data[3] + '%';
            $( "td:eq(2)", row ).text(data[2]);
            $( "td:eq(3)", row ).text(data[3]);
            $( "td:eq(2)", row ).addClass( "service-level" );
            $( "td:eq(3)", row ).addClass( "service-level" );
          } else if ( data[1].toLowerCase().indexOf( 'mttr' ) != -1 ) {
            $( "td:eq(2)", row ).addClass( "mttr-level" );
            if ( data[2] <= maxSuccessMTTR ) {
              $( "td:eq(2)", row ).addClass( "success" );
              $( "td:eq(2)", row ).removeClass( "danger" );
            } else {
              $( "td:eq(2)", row ).addClass( "danger" );
              $( "td:eq(2)", row ).removeClass( "success" );
            };
            if ( data[3] <= maxSuccessMTTR ) {
              $( "td:eq(3)", row ).addClass( "success" );
              $( "td:eq(3)", row ).removeClass( "danger" );
            } else {
              $( "td:eq(3)", row ).addClass( "danger" );
              $( "td:eq(3)", row ).removeClass( "success" );
            };
            data[3] = data[3] + ' минут';
            data[2] = data[2] + ' минут';
            $( "td:eq(2)", row ).text(data[2]);
            $( "td:eq(3)", row ).text(data[3]);
          } else if ( data[1].toLowerCase().indexOf( 'flr' ) != -1 ) {
            $( "td:eq(2)", row ).addClass( "flr-level" );
            $( "td:eq(3)", row ).addClass( "flr-level" );
            if ( data[2] >= minSuccessFLR ) {
              $( "td:eq(2)", row ).addClass( "success" );
              $( "td:eq(2)", row ).removeClass( "danger" );
            } else {
              $( "td:eq(2)", row ).addClass( "danger" );
              $( "td:eq(2)", row ).removeClass( "success" );
            };
            if ( data[3] >= minSuccessFLR ) {
              $( "td:eq(3)", row ).addClass( "success" );
              $( "td:eq(3)", row ).removeClass( "danger" );
            } else {
              $( "td:eq(3)", row ).addClass( "danger" );
              $( "td:eq(3)", row ).removeClass( "success" );
            };
            data[2] = data[2] + '%';
            data[3] = data[3] + '%';
            $( "td:eq(2)", row ).text(data[2]);
            $( "td:eq(3)", row ).text(data[3]);
          };
        },
      });
      table.column(0).visible(false);
  });
};

$("#desired-date").submit(function(event) {
  event.preventDefault();
  let dateCollection = getDateReports();
  reloadDatatable(dateCollection[0], dateCollection[1]);
  if (new Date(dateCollection[0]) > new Date(Date.now())) {
    alert("Выбрана недопустимая дата!");
    return
  }
  if (new Date(dateCollection[1]) > new Date(Date.now())) {
    alert("Выбрана недопустимая дата!");
    return
  }
});

$("#comparison-date").submit(function(event) {
  event.preventDefault();
  let dateCollection = getDateReports();
  reloadDatatable(dateCollection[0], dateCollection[1]);
  if (new Date(dateCollection[0]) > new Date(Date.now())) {
    alert("Выбрана недопустимая дата!");
    return
  }
  if (new Date(dateCollection[1]) > new Date(Date.now())) {
    alert("Выбрана недопустимая дата!");
    return
  }
});

$(document).ready(function () {
  let dateCollection = getDateReports();
  reloadDatatable(dateCollection[0], dateCollection[1]);
});