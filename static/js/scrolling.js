const leftCleaner = document.querySelector('#left_cleaner');
const rightCleaner = document.querySelector('#right_cleaner');

window.addEventListener('scroll', () => {
    let value = scrollY;
    leftCleaner.style.left = `-${value / 0.7}px`
    rightCleaner.style.right = `-${value / 0.7}px`
})
