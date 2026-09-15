import '../styles/main.css';
import { initAnimations } from './animations.js';
import { initNavigation } from './navigation.js';
import { initInteractions } from './interactions.js';
import { initContentGallery } from './content-gallery.js';

document.addEventListener('DOMContentLoaded', () => {
  const heroVideo = document.querySelector('.hero-media video');
  if (heroVideo) {
    const mobile = window.matchMedia('(max-width: 767px)');
    const syncPoster = () => {
      heroVideo.poster = mobile.matches ? heroVideo.dataset.mobilePoster : heroVideo.dataset.desktopPoster;
    };
    syncPoster();
    mobile.addEventListener('change', syncPoster);
  }
  const lenis = initAnimations();
  initNavigation(lenis);
  initInteractions();
  initContentGallery();
});
