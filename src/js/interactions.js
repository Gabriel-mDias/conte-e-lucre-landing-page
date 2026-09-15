const WHATSAPP_NUMBER = '5527998844331';

export function initInteractions() {
  initDiagnosticForm();
  initFaq();
}

function initDiagnosticForm() {
  const form = document.getElementById('formDiagnostico');
  if (!form) return;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const message = [
      'Olá! Conheci a Conte & Lucre pelo site e gostaria de solicitar um diagnóstico inicial.',
      '',
      '*Sobre meu negócio*',
      `Nome: ${data.get('nome')}`,
      `Empresa / segmento: ${data.get('empresa')}`,
      `Faturamento médio: ${data.get('faturamento')}`,
      `Principal desafio: ${data.get('desafio')}`,
      '',
      'Gostaria de entender qual caminho faz sentido para o meu cenário.',
    ].join('\n');
    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
    const popup = window.open(url, '_blank', 'noopener,noreferrer');
    if (!popup) window.location.href = url;
  });
}

function initFaq() {
  document.querySelectorAll('.faq-question').forEach((button) => {
    button.addEventListener('click', () => {
      const answerId = button.getAttribute('aria-controls');
      const answer = answerId ? document.getElementById(answerId) : null;
      if (!answer) return;

      const willOpen = button.getAttribute('aria-expanded') !== 'true';
      document.querySelectorAll('.faq-question[aria-expanded="true"]').forEach((openButton) => {
        if (openButton === button) return;
        openButton.setAttribute('aria-expanded', 'false');
        const openAnswer = document.getElementById(openButton.getAttribute('aria-controls'));
        if (openAnswer) openAnswer.hidden = true;
      });
      button.setAttribute('aria-expanded', String(willOpen));
      answer.hidden = !willOpen;
    });
  });
}
