import json
import urllib.request

from django.conf import settings
from django.shortcuts import render


def _send_via_resend(subject, body, reply_to):
    """Envía el correo por la API HTTP de Resend (puerto 443, no bloqueado)."""
    payload = {
        "from": settings.RESEND_FROM,
        "to": [settings.CONTACT_EMAIL],
        "subject": subject,
        "text": body,
    }
    if reply_to:
        payload["reply_to"] = [reply_to]

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    # timeout corto: si algo falla, no cuelga el worker (lo que causaba el 500).
    with urllib.request.urlopen(req, timeout=10) as resp:
        if resp.status >= 300:
            raise RuntimeError(f"Resend respondió {resp.status}")


def index(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        subject = f"Nuevo contacto: {name or 'Sin nombre'}"
        body = (
            f"Nombre: {name}\n"
            f"Email: {email}\n"
            f"Mensaje:\n{message}\n"
        )

        if not settings.RESEND_API_KEY:
            return render(
                request,
                "home/index.html",
                {"error": "El formulario no está configurado todavía. Intenta más tarde."},
            )

        try:
            _send_via_resend(subject, body, email)
            return render(request, "home/index.html", {"success": True})
        except Exception:
            return render(
                request,
                "home/index.html",
                {"error": "No se pudo enviar el correo. Intenta nuevamente."},
            )

    return render(request, "home/index.html")
