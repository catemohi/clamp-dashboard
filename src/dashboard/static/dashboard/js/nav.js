const sideMenu = document.querySelector("aside");
const closeBtn = document.querySelector("#close-btn");
const navBar = document.querySelector(".sidebar ul");

//check active aside menu
$(function () {
    $('#sidebar').on('click', 'li', function (event) {
        event.preventDefault();
        var current_url = this.querySelector('a').href;
        window.location.href = current_url;
    });
});

$(function() { 
    var location = window.location.href;
    var cur_url = '/' + location.split('/')[3]  + '/';
    $('#sidebar > ul li > a').each(function (ind, e) {
        var link = $(this).attr('data_target')
        $(this).parent().removeClass("active")
        if (cur_url == link)
            $(this).parent().addClass("active");
     });
});

function counterUpdate(data) {
    Counter = data.first_line_counter
    vipCounter = data.vip_line_counter
    if (Counter < 1) {
        $('#sidebar .task-status-on-the-group-count').text('').css({'opacity': '0', 'display': 'none'});
    }
    else {
        $('#sidebar .task-status-on-the-group-count').text(Counter).css({'opacity': '1', 'display': 'block'});
    }
    if (vipCounter < 1) {
        $('#sidebar .task-status-on-the-vip-count').text('').css({'opacity': '0', 'display': 'none'});
    }
    else {
        $('#sidebar .task-status-on-the-vip-count').text(vipCounter).css({'opacity': '1', 'display': 'block'});
    }
};
