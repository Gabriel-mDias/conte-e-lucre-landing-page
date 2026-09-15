export function initNavigation(lenis) {
  const navbar = document.querySelector('.navbar');
  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');

  const closeMenu = () => {
    menuToggle?.classList.remove('active');
    navLinks?.classList.remove('active');
    menuToggle?.setAttribute('aria-expanded', 'false');
    menuToggle?.setAttribute('aria-label', 'Abrir menu');
  };

  const updateNavbar = () => navbar?.classList.toggle('scrolled', window.scrollY > 24);
  window.addEventListener('scroll', updateNavbar, { passive: true });
  updateNavbar();

  menuToggle?.addEventListener('click', () => {
    const opening = !navLinks?.classList.contains('active');
    navLinks?.classList.toggle('active', opening);
    menuToggle.classList.toggle('active', opening);
    menuToggle.setAttribute('aria-expanded', String(opening));
    menuToggle.setAttribute('aria-label', opening ? 'Fechar menu' : 'Abrir menu');
  });

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const selector = link.getAttribute('href');
      if (!selector || selector === '#') return;
      const target = document.querySelector(selector);
      if (!target) return;
      event.preventDefault();
      closeMenu();
      if (lenis) lenis.scrollTo(target, { offset: -68, duration: 1.05 });
      else target.scrollIntoView({ behavior: 'auto' });
      history.replaceState(null, '', selector);
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });
}
