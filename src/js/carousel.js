import Swiper from 'swiper';
import { Navigation, Autoplay } from 'swiper/modules';

export function initTeamCarousel() {
  const swiperElement = document.querySelector('.team-swiper');
  if (!swiperElement) return null;

  const swiper = new Swiper('.team-swiper', {
    modules: [Navigation, Autoplay],
    slidesPerView: 1.15,
    spaceBetween: 20,
    grabCursor: true,
    speed: 700,
    autoplay: {
      delay: 5000,
      disableOnInteraction: true,
      pauseOnMouseEnter: true,
    },
    navigation: {
      nextEl: '.team-btn-next',
      prevEl: '.team-btn-prev',
    },
    breakpoints: {
      640: {
        slidesPerView: 2.15,
        spaceBetween: 24,
      },
      1024: {
        slidesPerView: 3.25,
        spaceBetween: 28,
      },
      1280: {
        slidesPerView: 3.8,
        spaceBetween: 32,
      },
    },
  });

  return swiper;
}
