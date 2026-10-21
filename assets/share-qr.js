/* Self-contained QR switcher: codes are generated as local SVG assets at build time. */
(() => {
  const dialog = document.getElementById('share-qr-dialog');
  const open = document.querySelector('[data-qr-open]');
  if (!dialog || !open || typeof dialog.showModal !== 'function') return;
  const isIt = document.documentElement.lang === 'it';
  const image = document.getElementById('share-qr-image');
  const url = document.getElementById('share-qr-url');
  const download = document.getElementById('share-qr-download');
  const status = dialog.querySelector('[data-qr-status]');
  const copy = dialog.querySelector('[data-qr-copy]');
  const targets = {
    portfolio: { url: 'https://alessio-olivieri.github.io/', svg: '/assets/qr-portfolio.svg', filename: 'alessio-portfolio-qr.svg' },
    cv: { url: 'https://alessio-olivieri.github.io/cv.pdf', svg: '/assets/qr-cv.svg', filename: 'alessio-cv-qr.svg' }
  };
  let selected = targets.portfolio;
  function select(which) {
    selected = targets[which] || targets.portfolio;
    image.src = selected.svg;
    image.alt = isIt
      ? (which === 'cv' ? 'Codice QR per aprire il CV PDF' : 'Codice QR per aprire il portfolio')
      : (which === 'cv' ? 'QR code linking to the PDF CV' : 'QR code linking to the portfolio');
    url.href = selected.url;
    url.textContent = selected.url.replace(/^https:\/\//, '');
    download.href = selected.svg;
    download.download = selected.filename;
    status.textContent = '';
    dialog.querySelectorAll('[data-qr-target]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.qrTarget === which));
    });
  }
  open.addEventListener('click', () => { select('portfolio'); dialog.showModal(); });
  dialog.querySelectorAll('[data-qr-target]').forEach(button => {
    button.addEventListener('click', () => select(button.dataset.qrTarget));
  });
  dialog.querySelector('[data-qr-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  copy.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(selected.url);
      status.textContent = isIt ? 'Link copiato.' : 'Link copied.';
    } catch {
      status.textContent = isIt ? 'Copia il link qui sopra.' : 'Copy the link shown above.';
    }
  });
})();
