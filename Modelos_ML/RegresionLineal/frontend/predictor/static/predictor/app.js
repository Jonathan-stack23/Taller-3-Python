const form = document.querySelector('#prediction-form');
const areaInput = document.querySelector('#area');
const button = document.querySelector('#submit-button');
const result = document.querySelector('#result');
const price = document.querySelector('#price');
const resultDetail = document.querySelector('#result-detail');
const feedback = document.querySelector('#feedback');
const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

const copFormatter = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 });

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  feedback.textContent = '';
  result.hidden = true;
  const area = Number(areaInput.value);
  if (!Number.isFinite(area) || area <= 0) {
    feedback.textContent = 'Ingresa un área válida mayor a 0 m².';
    areaInput.focus();
    return;
  }
  button.disabled = true;
  button.innerHTML = 'Calculando…';
  try {
    const response = await fetch(form.dataset.predictUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify({ area_m2: area }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || 'No fue posible calcular la estimación.');
    price.textContent = copFormatter.format(data.predicted_price);
    resultDetail.textContent = `Estimación para un apartamento de ${data.area_m2} m².`;
    result.hidden = false;
  } catch (error) {
    feedback.textContent = error.message || 'Ocurrió un error al consultar la estimación.';
  } finally {
    button.disabled = false;
    button.innerHTML = 'Estimar precio <span aria-hidden="true">→</span>';
  }
});
