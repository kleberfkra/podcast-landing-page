document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('show'); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });
    const hiddenElements = document.querySelectorAll('.slide-up');
    hiddenElements.forEach((el) => observer.observe(el));
    const header = document.querySelector('.header-container');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) { header.style.background = 'rgba(22, 34, 56, 0.9)'; header.style.border = '1px solid rgba(255, 138, 0, 0.3)'; } 
        else { header.style.background = 'rgba(22, 34, 56, 0.6)'; header.style.border = '1px solid rgba(255, 138, 0, 0.15)'; }
    });
});
