import 'swiper/css';
import '../styles/main.css';
import { initAnimations } from './animations.js';
import { initTeamCarousel } from './carousel.js';
import { initNavigation } from './navigation.js';

document.addEventListener('DOMContentLoaded', () => {
  const lenis = initAnimations();
  initTeamCarousel();
  initNavigation(lenis);
});
