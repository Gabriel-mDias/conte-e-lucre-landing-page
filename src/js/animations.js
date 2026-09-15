import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export function initAnimations() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) {
    document.querySelector('.hero-media video')?.pause();
    return null;
  }

  const lenis = new Lenis({
    duration: 1.05,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    wheelMultiplier: 0.95,
    touchMultiplier: 1.5,
  });

  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);

  document.querySelectorAll('[data-reveal]').forEach((element) => {
    gsap.from(element, {
      scrollTrigger: { trigger: element, start: 'top 90%', once: true },
      opacity: 0,
      y: 24,
      duration: 0.9,
      delay: Number(element.dataset.delay || 0),
      ease: 'power3.out',
      clearProps: 'opacity,transform',
    });
  });

  return lenis;
}
