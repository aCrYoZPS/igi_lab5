window.addEventListener('load', function () {
  setTimeout(function() {
    document.querySelector('.preloader_container').style.display = 'none';
    document.querySelector('body').style.visibility = 'visible';
    document.querySelector('.nav_header').style.visibility = 'visible';
    document.querySelector('.navigation_buttons').style.visibility = 'visible';
  }, 500);
});
