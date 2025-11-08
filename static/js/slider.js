let slideIndex = 1;
let paused = true;
let loop = false;
let delay = 5000;
let stopOnHover = false;

function toggleDelayInput() {
    const autoCheckbox = document.getElementById('auto');
    const delayInput = document.getElementById('delay');
    const stopOnHoverCheckbox = document.getElementById('stopMouseHover');
    delayInput.disabled = !autoCheckbox.checked;
    stopOnHoverCheckbox.disabled = !autoCheckbox.checked;
}

function applySettings() {
    loop = document.getElementById('loop').checked;
    let show_navs = document.getElementById('navs').checked;
    let navs = document.querySelectorAll('.navs-prev, .navs-next');
    for (let i = 0; i < navs.length; i++) {
        if (!show_navs) {
            navs[i].style.display = "none";
        } else {
            navs[i].style.display = "block";
        }
    }

    let show_pags = document.getElementById('pags').checked;
    let pagination_dots = document.getElementById('pagination_dots')
    if (!show_pags) {
        pagination_dots.style.visibility = "hidden"
    }
    else {
        pagination_dots.style.visibility = "visible"
    }

    paused = !document.getElementById('auto').checked;
    stopOnHover = document.getElementById('stopMouseHover').checked;
    delay = (parseInt(document.getElementById('delay').value, 10) || 5) * 1000;
    showNthSlides(slideIndex)
}

function plusSlides(n) {
    slideIndex += n;

    if (slideIndex > 3 && !loop) {
        slideIndex = 3;
    }

    if (slideIndex < 1 && !loop) {
        slideIndex = 1;
    }

    showNthSlides(slideIndex);
}

function currentSlide(n) {
    slideIndex = n;
    showNthSlides(slideIndex);
}

function showNthSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}


function showSlides() {
    if (!paused) {
        let i;
        let slides = document.getElementsByClassName("mySlides");
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        slideIndex++;
        if (slideIndex > slides.length) { slideIndex = 1 }
        slides[slideIndex - 1].style.display = "block";
    }
    setTimeout(showSlides, delay);
}

document.addEventListener('DOMContentLoaded', () => {
    const sliderContainer = document.getElementById('sliderContainer');

    sliderContainer.addEventListener('mouseenter', () => {
        if (stopOnHover) {
            paused = true;
        }
    });

    sliderContainer.addEventListener('mouseleave', () => {
        if (stopOnHover) {
            paused = false;
        }
    });

    toggleDelayInput();
    document.getElementById('auto').addEventListener('change', toggleDelayInput);
    showNthSlides(1);
    showSlides();
})
