import os
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    context = {}
    if request.method == 'POST':
        area_m2 = request.POST.get('area_m2')
        if area_m2:
            try:
                api_base = os.environ.get("API_URL", "http://127.0.0.1:8000")
                api_base = api_base.rstrip("/")
                if not api_base.endswith("/predict"):
                    api_url = f"{api_base}/predict"
                else:
                    api_url = api_base

                payload = {"area_m2": float(area_m2)}
                
                response = requests.post(api_url, json=payload, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    precio_formateado = f"${data['predicted_price']:,.2f}"
                    context['resultado'] = precio_formateado
                    context['area'] = area_m2
                else:
                    context['error'] = "La API respondió con un errorsote."
                    
            except requests.exceptions.RequestException:
                context['error'] = "No se pudo conectar con la API."

    return render(request, 'index.html', context)