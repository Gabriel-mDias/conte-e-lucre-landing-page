export function initNavigation(lenis) {
  const navbar = document.querySelector('.navbar');
  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  const allLinks = document.querySelectorAll('a[href^="#"]');

  // 1. Estado da Navbar ao Rolar
  function handleScroll() {
    if (window.scrollY > 50) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  // 2. Toggle do Menu Mobile
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      menuToggle.classList.toggle('active');
      navLinks.classList.toggle('active');
    });
  }

  // 3. Rolagem Suave para Âncoras com Lenis
  allLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href');
      if (!targetId || targetId === '#') return;

      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        
        // Fecha menu mobile caso esteja aberto
        menuToggle?.classList.remove('active');
        navLinks?.classList.remove('active');

        if (lenis) {
          lenis.scrollTo(targetEl, {
            offset: -80,
            duration: 1.2,
          });
        } else {
          targetEl.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });
}
