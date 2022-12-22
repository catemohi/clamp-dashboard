// changet heme
const themeToggler = document.querySelector(".theme-toggler");
const menuBtn = document.querySelector(".menu-btn");

themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-var');

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
    
    if (themeToggler.querySelector('span:nth-child(2)').classList.contains('active')) {
        document.cookie = "theme=dark; path=/;";
    } else {
        document.cookie = "theme=white; path=/;";
    }

})

// show sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

//close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})


if (localStorage.layoutSwitch === 'true') {
    document.body.classList.toggle('dark-theme-var');
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
}
    