import os
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    context = {}
    api_base = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")
    context["api_url_debug"] = api_base

    if request.method == "POST":
        area_m2 = request.POST.get("area_m2")
        if area_m2:
            try:
                if not api_base.endswith("/predict"):
                    api_url = f"{api_base}/predict"
                else:
                    api_url = api_base

                payload = {"area_m2": float(area_m2)}

                response = requests.post(api_url, json=payload, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    precio_formateado = f"${data['predicted_price']:,.2f}"
                    context["resultado"] = precio_formateado
                    context["area"] = area_m2
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    context["error"] = f"Error API ({response.status_code}): {detail}"

            except requests.exceptions.ConnectionError:
                context["error"] = (
                    f"No se puede conectar a la API ({api_base}). "
                    "Verifica que la API_URL sea correcta y que el backend esté encendido."
                )
            except requests.exceptions.Timeout:
                context["error"] = (
                    f"Tiempo de espera agotado al contactar la API ({api_base})."
                )
            except requests.exceptions.RequestException as e:
                context["error"] = f"Error en la peticion: {str(e)}"
            except ValueError:
                context["error"] = "El area_m2 debe ser un numero valido."

    return render(request, "index.html", context)
