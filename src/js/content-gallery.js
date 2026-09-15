import Swiper from 'swiper';
import { A11y, Keyboard, Navigation, Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/a11y';
import 'swiper/css/keyboard';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

const posts = {
  'post-1': {
    theme: 'Controle financeiro',
    title: 'O custo de viver sem planejamento',
    summary: 'Não ter controle pode significar viver no limite, adiar sonhos e decidir às pressas. Planejar não é limitar a vida: é escolher o futuro que você quer viver.',
    pages: [1, 2, 3, 4].map((page) => ({ stem: `post_1_pag_${page}`, alt: `Página ${page} de 4 da publicação sobre as consequências do descontrole financeiro` })),
  },
  'post-2': {
    theme: 'Organização',
    title: 'Cinco passos para sair do vermelho',
    summary: 'Encare a realidade, anote os gastos, renegocie dívidas, crie metas possíveis e busque orientação para construir um plano de ação. Não é mágica, é método.',
    pages: [{ stem: 'post_2_pag_unica', alt: 'Publicação completa com cinco dicas para sair do vermelho' }],
  },
  'post-4': {
    theme: 'Estratégia',
    title: 'Nem todo movimento significa progresso',
    summary: 'Trabalhar muito e pagar contas não garante avanço. Sem estratégia, o dinheiro apenas circula; com planejamento, ele constrói. Quem decide melhor, cresce melhor.',
    pages: [1, 2, 3, 4, 5].map((page) => ({ stem: `post_4_pag_${page}`, alt: `Página ${page} de 5 da publicação sobre a diferença entre movimento e progresso financeiro` })),
  },
};

function pageMarkup(page) {
  return `<div class="swiper-slide"><picture><source type="image/webp" srcset="assets/images/posts/${page.stem}-540.webp 540w, assets/images/posts/${page.stem}-1080.webp 1080w" sizes="(max-width: 560px) 96vw, 70vw"><img src="assets/images/posts/${page.stem}-1080.jpg" alt="${page.alt}" width="1080" height="1350"></picture></div>`;
}

export function initContentGallery() {
  const carousel = document.querySelector('[data-content-carousel]');
  const dialog = document.getElementById('contentGallery');
  if (!carousel || !dialog) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  new Swiper(carousel, {
    modules: [A11y, Keyboard, Navigation, Pagination],
    slidesPerView: 1.08,
    spaceBetween: 14,
    speed: reduceMotion ? 0 : 550,
    keyboard: { enabled: true, onlyInViewport: true },
    navigation: { prevEl: '.carousel-prev', nextEl: '.carousel-next' },
    pagination: { el: '.content-pagination', clickable: true },
    a11y: { prevSlideMessage: 'Conteúdo anterior', nextSlideMessage: 'Próximo conteúdo', paginationBulletMessage: 'Ir para o conteúdo {{index}}' },
    breakpoints: { 620: { slidesPerView: 2, spaceBetween: 20 }, 1024: { slidesPerView: 3, spaceBetween: 26 } },
  });

  const wrapper = dialog.querySelector('.swiper-wrapper');
  const galleryElement = dialog.querySelector('[data-gallery-swiper]');
  const closeButton = dialog.querySelector('.gallery-close');
  const title = dialog.querySelector('#galleryTitle');
  const theme = dialog.querySelector('#galleryTheme');
  const summary = dialog.querySelector('#gallerySummary');
  const counter = dialog.querySelector('.gallery-counter');
  let gallery = null;
  let returnFocus = null;

  const closeGallery = () => {
    if (dialog.open) dialog.close();
  };

  const openGallery = (postId, trigger) => {
    const post = posts[postId];
    if (!post) return;
    returnFocus = trigger;
    title.textContent = post.title;
    theme.textContent = post.theme;
    summary.textContent = post.summary;
    wrapper.innerHTML = post.pages.map(pageMarkup).join('');
    galleryElement.classList.toggle('is-single', post.pages.length === 1);
    gallery?.destroy(true, true);
    gallery = new Swiper(galleryElement, {
      modules: [A11y, Keyboard, Navigation, Pagination],
      slidesPerView: 1,
      spaceBetween: 24,
      speed: reduceMotion ? 0 : 450,
      grabCursor: post.pages.length > 1,
      allowTouchMove: post.pages.length > 1,
      keyboard: { enabled: true },
      navigation: { prevEl: '.gallery-prev', nextEl: '.gallery-next' },
      pagination: { el: '.gallery-pagination', clickable: true },
      a11y: { prevSlideMessage: 'Página anterior', nextSlideMessage: 'Próxima página', paginationBulletMessage: 'Ir para a página {{index}}' },
      on: { init(swiper) { counter.textContent = `1 / ${swiper.slides.length}`; }, slideChange(swiper) { counter.textContent = `${swiper.realIndex + 1} / ${swiper.slides.length}`; } },
    });
    document.body.classList.add('gallery-open');
    dialog.showModal();
    closeButton.focus();
  };

  carousel.querySelectorAll('[data-post]').forEach((button) => button.addEventListener('click', () => openGallery(button.dataset.post, button)));
  closeButton.addEventListener('click', closeGallery);
  dialog.addEventListener('click', (event) => { if (event.target === dialog) closeGallery(); });
  dialog.addEventListener('cancel', (event) => { event.preventDefault(); closeGallery(); });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('gallery-open');
    gallery?.keyboard.disable();
    returnFocus?.focus();
  });
}
