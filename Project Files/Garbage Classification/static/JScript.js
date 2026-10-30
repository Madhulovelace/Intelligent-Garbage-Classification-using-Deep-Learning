'use strict';
const demo = document.getElementById('demo');
const upload = document.getElementById('imageupload');
const result = document.getElementById('result');
const cards = document.querySelectorAll('[data-type]');

if (upload && demo) {
  upload.addEventListener('change', (event) => {
    const file = event.target.files && event.target.files[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      upload.value = '';
      window.alert('Please select a valid image.');
      return;
    }
    const preview = URL.createObjectURL(file);
    demo.onload = () => URL.revokeObjectURL(preview);
    demo.src = preview;
    cards.forEach((card) => card.classList.remove('hidden'));
  });
}

if (result && result.textContent.trim()) {
  const selected = result.textContent.trim().toLowerCase();
  cards.forEach((card) => card.classList.toggle('hidden', card.dataset.type !== selected));
} else {
  cards.forEach((card) => card.classList.add('hidden'));
}
