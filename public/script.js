const dropZone    = document.getElementById('dropZone');
const fileInput   = document.getElementById('fileInput');
const btnDetectar = document.getElementById('btnDetectar');
const imgOrig     = document.getElementById('imgOriginal');
const imgProc     = document.getElementById('imgProcesada');
const metricsBox  = document.getElementById('metrics');
const resultsBox  = document.getElementById('results');
const loader      = document.getElementById('loader');
const msgBox      = document.getElementById('msg');
const countEl     = document.getElementById('count');
const modeloEl    = document.getElementById('modelo');

let archivoActual = null;
let urlOriginal   = null;

function limpiarUrl(){
  if(urlOriginal){URL.revokeObjectURL(urlOriginal);urlOriginal=null}
}

function setMsg(tipo, texto){
  msgBox.className = 'msg ' + (tipo === 'ok' ? 'ok' : tipo === 'err' ? 'err' : '');
  msgBox.textContent = texto || '';
}

fileInput.addEventListener('change', e => {
  const f = e.target.files?.[0];
  if(!f) return;
  seleccionarArchivo(f);
});

function seleccionarArchivo(f){
  if(!f.type.startsWith('image/')){
    setMsg('err','El archivo debe ser una imagen.');return;
  }
  limpiarUrl();
  archivoActual = f;
  urlOriginal = URL.createObjectURL(f);
  imgOrig.src = urlOriginal;
  btnDetectar.disabled = false;
  resultsBox.classList.remove('d-none');
  metricsBox.classList.remove('d-none');
  countEl.textContent = '0';
  modeloEl.textContent = '—';
  imgProc.removeAttribute('src');
  imgProc.alt = 'Esperando analisis...';
  setMsg('','');
}

['dragenter','dragover'].forEach(ev => {
  dropZone.addEventListener(ev, e => {e.preventDefault();dropZone.classList.add('dragover')});
});
['dragleave','drop'].forEach(ev => {
  dropZone.addEventListener(ev, e => {e.preventDefault();dropZone.classList.remove('dragover')});
});
dropZone.addEventListener('drop', e => {
  const f = e.dataTransfer?.files?.[0];
  if(f) seleccionarArchivo(f);
});

btnDetectar.addEventListener('click', async () => {
  if(!archivoActual) return;
  btnDetectar.disabled = true;
  loader.classList.remove('d-none');
  imgProc.alt = 'Procesando...';
  setMsg('','');
  const fd = new FormData();
  fd.append('imagen', archivoActual);
  try{
    const res = await fetch('/api/detectar', {method:'POST', body: fd});
    const data = await res.json();
    if(!res.ok) throw new Error(data.error || 'Error en el servidor');
    countEl.textContent  = String(data.total_rostros ?? data.faces_detected ?? 0);
    modeloEl.textContent = data.modelo_usado || '—';
    const imgSrc = data.image || (data.imagen_procesada
      ? `data:image/jpeg;base64,${data.imagen_procesada}` : '');
    if(imgSrc){imgProc.src = imgSrc; imgProc.alt = 'Rostros detectados'}
    const n = data.total_rostros ?? data.faces_detected ?? 0;
    setMsg('ok', `Listo · ${n} rostro(s) detectado(s) con ${data.modelo_usado || 'detector'}.`);
  }catch(err){
    setMsg('err', 'Error: ' + err.message);
  }finally{
    btnDetectar.disabled = false;
    loader.classList.add('d-none');
  }
});
