const sideMenu = document.querySelector("aside");
const closeBtn = document.querySelector("#close-btn");
const navBar = document.querySelector(".sidebar ul");

function fadeIn(el, speed) {
	// Fade in block
	var step = 1 / speed;
	var interval = setInterval(function() {
		if (+el.style.opacity >= 1)
			clearInterval(interval);
			
		el.style.opacity = + el.style.opacity + step;
	}, speed / 1000);
}

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


function counterUpdate() {
    let firstLineCounter = document.querySelector('.task-status-on-the-group-count');
    let vipLineCounter = document.querySelector('.task-status-on-the-vip-count');
    if (firstLineCounter.textContent > 1) {
        firstLineCounter.style.display = 'block';
        fadeIn(firstLineCounter, 100);
    }
    else {
        firstLineCounter.style.display = 'none';
        firstLineCounter.style.opacity = '0';
    };
    if (vipLineCounter.textContent > 1) {
        vipLineCounter.style.display = 'block';
        fadeIn(vipLineCounter, 100);
    }
    else {
        vipLineCounter.style.display = 'none';
        vipLineCounter.style.opacity = '0';
    }
};

function valueCounterUpdate(data) {
    document.querySelector('.task-status-on-the-group-count').textContent = data.first_line_counter
    document.querySelector('.task-status-on-the-vip-count').textContent = data.vip_line_counter
    counterUpdate()
};
counterUpdate()