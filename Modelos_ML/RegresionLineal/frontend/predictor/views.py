import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST


@ensure_csrf_cookie
def home(request):
    return render(request, "predictor/index.html")


@require_POST
def predict(request):
    """Valida la consulta y la reenvía al modelo expuesto por FastAPI."""
    try:
        payload = json.loads(request.body)
        area = float(payload["area_m2"])
        if area <= 0:
            raise ValueError
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return JsonResponse({"detail": "El área debe ser un número mayor a 0."}, status=400)

    api_url = settings.PREDICTION_API_URL.strip().rstrip("/")
    if not api_url.startswith(("http://", "https://")):
        api_url = f"https://{api_url}"

    api_request = Request(
        f"{api_url}/predict",
        data=json.dumps({"area_m2": area}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(api_request, timeout=10) as response:
            return JsonResponse(json.loads(response.read().decode("utf-8")), status=response.status)
    except HTTPError as error:
        try:
            detail = json.loads(error.read().decode("utf-8")).get("detail")
        except (json.JSONDecodeError, UnicodeDecodeError):
            detail = "El servicio de predicción devolvió un error."
        return JsonResponse({"detail": detail}, status=error.code)
    except (URLError, ValueError):
        return JsonResponse(
            {"detail": "No se pudo conectar con el servicio de predicción."}, status=503
        )
