// ==========================================
// VisionML - Detección de Rostros
// Personalizado por: Jonathan Martinez
// Taller 3 Machine Learning · SENA
// ==========================================

// 1. Referencias a elementos comunes
const loader = document.getElementById("loader");
const imgResult = document.getElementById("imgResult");
const metricsZone = document.getElementById("metricsZone");
const faceCount = document.getElementById("faceCount");
const metricsTitle = document.getElementById("metricsTitle");
const metricsDesc = document.getElementById("metricsDesc");
const statusBadge = document.getElementById("statusBadge");
const emptyOriginal = document.getElementById("emptyOriginal");
const emptyResult = document.getElementById("emptyResult");

// 2. Referencias modo archivo (Upload)
const sectionUpload = document.getElementById("sectionUpload");
const btnModeUpload = document.getElementById("btnModeUpload");
const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const btnProcess = document.getElementById("btnProcess");
const imgOriginal = document.getElementById("imgOriginal");
const boxOriginal = document.getElementById("boxOriginal");

// 3. Referencias modo cámara (Webcam)
const sectionCamera = document.getElementById("sectionCamera");
const btnModeCamera = document.getElementById("btnModeCamera");
const video = document.getElementById("webcam");
const canvas = document.getElementById("canvasFrame");
const btnStartCamera = document.getElementById("btnStartCamera");
const btnStopCamera = document.getElementById("btnStopCamera");
const btnToggleCamera = document.getElementById("btnToggleCamera");

// 4. Variables de estado
let selectedFile = null;
let streamInstance = null;
let streamInterval = null;
let isStreaming = false;
let currentFacingMode = "user"; // "user" = frontal | "environment" = trasera

// 5. Control de interfaz (conmutación de modos)
btnModeUpload.addEventListener("click", () => switchMode("upload"));
btnModeCamera.addEventListener("click", () => switchMode("camera"));

function switchMode(mode) {
  if (mode === "upload") {
    btnModeUpload.classList.add("active");
    btnModeCamera.classList.remove("active");
    sectionUpload.classList.remove("d-none");
    sectionCamera.classList.add("d-none");
    boxOriginal.classList.remove("d-none");
    stopCameraFlow();
    setStatus("Listo para analizar una imagen");
  } else {
    btnModeCamera.classList.add("active");
    btnModeUpload.classList.remove("active");
    sectionCamera.classList.remove("d-none");
    sectionUpload.classList.add("d-none");
    boxOriginal.classList.add("d-none");
    imgResult.classList.add("d-none");
    metricsZone.classList.add("d-none");
    setStatus("Esperando activación de la cámara…");
  }
}

// 6. Lógica modo archivo (Drag & Drop)
["dragenter", "dragover"].forEach((name) => {
  dropZone.addEventListener(name, (e) => {
    e.preventDefault();
    dropZone.classList.add("is-dragging");
  });
});

["dragleave", "drop"].forEach((name) => {
  dropZone.addEventListener(name, (e) => {
    e.preventDefault();
    dropZone.classList.remove("is-dragging");
  });
});

dropZone.addEventListener("drop", (e) => handleFile(e.dataTransfer.files[0]));
fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));

function handleFile(file) {
  if (file && file.type.startsWith("image/")) {
    selectedFile = file;
    btnProcess.disabled = false;
    const reader = new FileReader();
    reader.onload = (e) => {
      imgOriginal.src = e.target.result;
      imgOriginal.classList.remove("d-none");
      emptyOriginal.classList.add("d-none");
      imgResult.classList.add("d-none");
      emptyResult.classList.remove("d-none");
      metricsZone.classList.add("d-none");
      setStatus("Imagen lista — pulsa Analizar rostros");
    };
    reader.readAsDataURL(file);
  } else {
    alert("❌ Archivo no válido. Por favor selecciona una imagen (JPG, PNG, WEBP).");
  }
}

btnProcess.addEventListener("click", async () => {
  if (!selectedFile) return;
  const formData = new FormData();
  formData.append("image", selectedFile);

  loader.classList.remove("d-none");
  imgResult.classList.add("d-none");
  emptyResult.classList.add("d-none");
  setStatus("🔄 Analizando imagen con OpenCV…");

  await sendFrameToBackend(formData);
  loader.classList.add("d-none");
});

// 7. Lógica modo cámara (flujo en tiempo real)
btnStartCamera.addEventListener("click", async () => {
  await initCamera();
  btnStartCamera.disabled = true;
  btnStopCamera.disabled = false;
  btnToggleCamera.style.display = "inline-block";
  setStatus("📹 Cámara activa — detectando en vivo…");
});

btnToggleCamera.addEventListener("click", async () => {
  currentFacingMode = currentFacingMode === "user" ? "environment" : "user";
  if (isStreaming) {
    clearInterval(streamInterval);
    if (streamInstance) streamInstance.getTracks().forEach((track) => track.stop());
    await initCamera();
    setStatus("🔄 Cámara cambiada — procesando nueva fuente…");
  }
});

async function initCamera() {
  try {
    streamInstance = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 480 }, height: { ideal: 360 }, facingMode: currentFacingMode },
      audio: false,
    });
    video.srcObject = streamInstance;
    isStreaming = true;
    imgResult.classList.remove("d-none");
    streamInterval = setInterval(processCameraFrame, 600);
  } catch (err) {
    console.error("Error al acceder a la cámara:", err);
    alert("❌ No se pudo acceder a la cámara. Asegúrate de dar permisos de webcam.");
    currentFacingMode = currentFacingMode === "user" ? "environment" : "user";
  }
}

btnStopCamera.addEventListener("click", stopCameraFlow);

function stopCameraFlow() {
  clearInterval(streamInterval);
  isStreaming = false;
  if (streamInstance) streamInstance.getTracks().forEach((track) => track.stop());
  video.srcObject = null;
  btnStartCamera.disabled = false;
  btnStopCamera.disabled = true;
  btnToggleCamera.style.display = "none";
  loader.classList.add("d-none");
  setStatus("Cámara apagada");
}

async function processCameraFrame() {
  if (!isStreaming) return;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(async (blob) => {
    if (!blob) return;
    const formData = new FormData();
    formData.append("image", blob, "frame.jpg");
    await sendFrameToBackend(formData);
  }, "image/jpeg", 0.72);
}

// 8. Comunicación asíncrona con Vercel API
async function sendFrameToBackend(formData) {
  try {
    const t0 = performance.now();
    const response = await fetch("/api/detect", { method: "POST", body: formData });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ error: "Error HTTP " + response.status }));
      setStatus("❌ Error: " + (err.error || "desconocido"));
      return;
    }
    const t1 = performance.now();
    const data = await response.json();
    if (data.success) {
      imgResult.src = data.image;
      imgResult.classList.remove("d-none");
      emptyResult.classList.add("d-none");
      metricsZone.classList.remove("d-none");
      faceCount.textContent = data.faces_detected;
      const tiempoMs = Math.round(t1 - t0);
      const modelo = data.modelo_usado || "Modelo OpenCV";
      metricsTitle.textContent = `Detección completada en ${tiempoMs} ms`;
      metricsDesc.textContent = `${data.faces_detected} rostro(s) detectado(s) usando ${modelo}`;
      setStatus(`✅ ${data.faces_detected} rostros · ${modelo} · ${tiempoMs} ms`);
    } else {
      setStatus("⚠️ " + (data.error || "No se pudo procesar la imagen"));
    }
  } catch (error) {
    console.error("Error en la transmisión de datos:", error);
    setStatus("❌ Error de conexión con el API");
  }
}

function setStatus(texto) {
  if (statusBadge) statusBadge.textContent = texto;
}

setStatus("Listo para analizar");
