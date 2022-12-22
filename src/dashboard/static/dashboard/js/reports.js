function getDate(offset) {
    var d = new Date();
    var day = d.getDate() + offset
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


// function getReport() {
//     var desired_date = getDate(-1)
//     var comparison_date = getDate(-2)
//     console.log(desired_date, comparison_date)
//     $.post('/json/reports', { desired_date: desired_date, comparison_date: comparison_date, csrfmiddlewaretoken: window.CSRF_TOKEN, }, function (data) {
//         console.log(data);
//     });
// }
// getReport()



document.getElementById('date-desired').value = getDate(0);
document.getElementById('date-comparison').value = getDate(-1);



$(document).ready(function () {
    var cookies = document.cookie.split(/[;] */).reduce(function(result, pairStr) {
        var arr = pairStr.split('=');
        if (arr.length === 2) { result[arr[0]] = arr[1]; }
        return result;
    }, {});
    var table = $('#trouble-table').DataTable({
        "ajax": {
            'type': 'POST',
            'url': '/json/reports',
            'data': function ( d ) {
                d.csrfmiddlewaretoken = cookies["csrftoken"],
                d.desired_date = document.getElementById('date-desired').value,
                d.comparison_date = document.getElementById('date-comparison').value
            },
        },
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf'
        ],
        "columns": [
            {"data": "number"},
            {"data": "name"},
            {"data": "desired_date"},
            {"data": "comparison_date"},
        ],
        "autoWidth": false,
        "bAutoWidth": false,
        "bPaginate": false
    });
    table.column(0).visible(false);

    $("#desired-date").submit(function(e) {
        e.preventDefault();
        table.ajax.reload()
    });
    
    $("#comparison-date").submit(function(e) {
        e.preventDefault();
        table.ajax.reload()
    });
    
});