// Way2TheUnknown — Funciones básicas
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            e.preventDefault();
            document.querySelector(a.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});
        });
    });
    // Highlight nav activo
    const path = window.location.pathname.split('/').pop();
    document.querySelectorAll('.nav-links a').forEach(a => {
        if(a.getAttribute('href') === path) a.style.color = 'var(--verde)';
    });
});
