import os
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# El decorador @csrf_exempt apaga la validación de seguridad para este formulario
@csrf_exempt
def home(request):
    context = {}
    if request.method == 'POST':
        area_m2 = request.POST.get('area_m2')
        if area_m2:
            try:
                # Usa la variable de entorno de Railway, o localhost si estás en tu PC
                api_url = os.environ.get("API_URL", "http://127.0.0.1:8000/predict")
                payload = {"area_m2": float(area_m2)}
                
                response = requests.post(api_url, json=payload)
                
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