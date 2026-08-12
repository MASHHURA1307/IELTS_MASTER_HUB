// IELTS Master Hub — Main Javascript

document.addEventListener('DOMContentLoaded', () => {
    // 1. Dark Mode Toggle
    const darkModeBtn = document.getElementById('darkModeToggle');
    const htmlElem = document.documentElement;

    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlElem.setAttribute('data-bs-theme', savedTheme);
    updateDarkModeIcon(savedTheme);

    if (darkModeBtn) {
        darkModeBtn.addEventListener('click', () => {
            const currentTheme = htmlElem.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            htmlElem.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateDarkModeIcon(newTheme);
        });
    }

    function updateDarkModeIcon(theme) {
        if (!darkModeBtn) return;
        const icon = darkModeBtn.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'bi bi-sun-fill text-warning';
        } else {
            icon.className = 'bi bi-moon-stars-fill text-body';
        }
    }

    // 2. Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.querySelector('.app-sidebar');

    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }

    // 3. Auto-hide Flash Messages after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.flash-messages-container .alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});
