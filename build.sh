#!/usr/bin/env bash
set -euxo pipefail

echo "=== Instalando dependencias del sistema para OpenCV ==="
apt-get update -y || true
apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libopencv-dev || true

echo "=== Instalando dependencias Python ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Build finalizado ==="
