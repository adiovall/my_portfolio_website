// static/js/script.js
AOS.init({
    duration: 800,
    once: true,
    disable: window.innerWidth < 600
});

// Contact form handling
document.getElementById('contact-form')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const form = this;
    const formData = new FormData(form);
    const messageElement = document.getElementById('form-message');

    messageElement.style.display = 'block';
    messageElement.textContent = 'Sending...';
    messageElement.className = 'text-center text-gray-300';

    fetch('/contact', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        messageElement.className = 'text-center ' + (data.status === 'success' ? 'text-green-400' : 'text-red-400');
        messageElement.textContent = data.message;
        if (data.status === 'success') {
            form.reset();
            grecaptcha.reset();
        }
    })
    .catch(error => {
        messageElement.className = 'text-center text-red-400';
        messageElement.textContent = 'Network error: Unable to connect to server.';
        console.error('Form submission error:', error);
    });
});

// Project filtering
const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        filterButtons.forEach(btn => btn.classList.remove('bg-teal-800', 'active'));
        button.classList.add('bg-teal-800', 'active');

        const filter = button.dataset.filter;

        projectCards.forEach(card => {
            const category = card.dataset.category;
            if (filter === 'all' || filter === category) {
                card.style.display = 'block';
                card.setAttribute('data-aos', 'fade-up');
            } else {
                card.style.display = 'none';
            }
        });

        AOS.refresh();
    });
});

// Theme toggle
const toggleButton = document.getElementById('theme-toggle');
if (toggleButton) {
    console.log('Theme toggle button found');
    toggleButton.addEventListener('click', () => {
        console.log('Theme toggle clicked');
        const htmlElement = document.documentElement;
        const isDark = htmlElement.classList.toggle('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        console.log('Theme set to:', isDark ? 'dark' : 'light');
    });
} else {
    console.error('Theme toggle button not found');
}

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    console.log('Applying saved dark theme');
    document.documentElement.classList.add('dark');
}