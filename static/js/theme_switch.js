function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = localStorage.getItem("theme") || html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
