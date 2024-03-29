$(document).ready(function () {

    $('#trouble-table thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#trouble-table thead');

    var table = $('#trouble-table').DataTable({
        "ajax": "/json/table",
        "columns": [
            {"data": "number", "className": "number"},
            {"data": "vip_contragent", "className": "vip-contragent"},
            {"data": "name", "className": "name"},
            {"data": "issue_type", "className": "issue-type"},
            {"data": "name_contragent", "className": "name-contragent"},
            {"data": "name_service", "className": "name-service"},
            {"data": "step_time", "className": "step-time"},
            {"data": "step", "className": "step"},
            {"data": "responsible", "className": "responsible"},
            {"data": "last_edit_time", "className": "last-edit-time"},
            {"data": "return_to_work_time", "className": "return-work-time"},

        ],
        "order": [[6, 'asc'], [10, 'asc']],
        'rowCallback': function(row, data, index){

            if ($(row).children('.step-time')) {
                var timestamp = data["step_time"];
                var days = Math.floor(timestamp / 60 / 60 / 24);
                var hours = Math.floor(timestamp / 60 / 60 - days * 24);
                var minutes = Math.floor(timestamp / 60) - (hours * 60) - (days * 24 * 60);
                time = days + ' дней ' + hours + ' ч ' + minutes + ' мин ';
                $(row).children('.step-time').text(time);
            };
            $(row).children('.name').text('');
            $(row).children('.name').append('<a href=' + data.url_issue + '>'+ data.name +'</a>');
            $(row).children('.return-work-time').text(new Intl.DateTimeFormat("ru", options).format(new Date(data.return_to_work_time)));
            returnedNotificationSettings.forEach(element => {
                if (element.step === data.step) {
                    let returnedUnixTime = new Date(data.return_to_work_time).valueOf();
                    let timedeltaReturned = Math.floor(( returnedUnixTime - Date.now())  / 1000);
                    if (timedeltaReturned < element.alarm_time || returnedUnixTime < Date.now()){
                        $(row).css('background-color', 'var(--color-warning)');
                    } else {
                        $(row).css('background-color', 'transparent');
                    }
                };
            });
            burnedNotificationSettings.forEach(element => {
                if (element.step === data.step) {
                    let timedelta = element.step_time - element.alarm_time;
                    if (data.step_time > timedelta){
                        $(row).css('background-color', 'var(--color-danger)');
                    } else {
                        $(row).css('background-color', 'transparent');
                    }
                };
            });
            


        },
        "autoWidth": false,
        "bAutoWidth": false,
        "orderCellsTop": true,
        "fixedHeader": true,
        "pageLength": 30,
        "lengthMenu": [ 15, 30, 45, 60 ],
        
        initComplete: function () {
            var api = this.api();
 
            // For each column
            api
                .columns()
                .eq(0)
                .each(function (colIdx) {
                    // Set the header cell to contain the input element
                    var cell = $('.filters th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    var title = $(cell).text();
                    $(cell).html('<input type="text" placeholder="' + title + '" />');
 
                    // On every keypress in this input
                    $(
                        'input',
                        $('.filters th').eq($(api.column(colIdx).header()).index())
                    )
                        .off('keyup change')
                        .on('change', function (e) {
                            // Get the search value
                            $(this).attr('title', $(this).val());
                            var regexr = '({search})'; //$(this).parents('th').find('select').val();
 
                            var cursorPosition = this.selectionStart;
                            // Search the column for that value
                            api
                                .column(colIdx)
                                .search(
                                    this.value != ''
                                        ? regexr.replace('{search}', '(((' + this.value + ')))')
                                        : '',
                                    this.value != '',
                                    this.value == ''
                                )
                                .draw();
                        })
                        .on('keyup', function (e) {
                            e.stopPropagation();
 
                            $(this).trigger('change');
                            $(this)
                                .focus()[0];
                        });
                });
        },
    });

    function resizeTable() {
        if (window.innerWidth > 1800) {
            table.column(0).visible(false);
            table.column(1).visible(false);
            table.column(2).visible(true);
            table.column(3).visible(false);
            table.column(4).visible(true);
            table.column(5).visible(true);
            table.column(4).visible(false);
            table.column(5).visible(true);
            table.column(6).visible(false);
            table.column(7).visible(true);
            table.column(8).visible(true);
            table.column(9).visible(false);
            table.column(10).visible(true);
        } else if (window.innerWidth < 1800 && window.innerWidth > 1200) {
            table.column(0).visible(false);
            table.column(1).visible(false);
            table.column(2).visible(true);
            table.column(3).visible(false);
            table.column(4).visible(false);
            table.column(5).visible(false);
            table.column(6).visible(false);
            table.column(7).visible(true);
            table.column(8).visible(true);
            table.column(9).visible(false);
            table.column(10).visible(true);
        } else if (window.innerWidth < 1200 && window.innerWidth > 500){
            table.column(0).visible(false);
            table.column(1).visible(false);
            table.column(2).visible(true);
            table.column(3).visible(false);
            table.column(4).visible(false);
            table.column(5).visible(false);
            table.column(6).visible(false);
            table.column(7).visible(true);
            table.column(8).visible(true);
            table.column(9).visible(false);
            table.column(10).visible(false);
        } else {
            table.column(0).visible(false);
            table.column(1).visible(false);
            table.column(2).visible(true);
            table.column(3).visible(false);
            table.column(4).visible(false);
            table.column(5).visible(false);
            table.column(6).visible(false);
            table.column(7).visible(false);
            table.column(8).visible(false);
            table.column(9).visible(false);
            table.column(10).visible(false);
        }
    }
    resizeTable();
    setInterval( function () {
        table.ajax.reload();
    }, 30000 );
    $(window).resize(function() {
        resizeTable();
        });
        
});
