from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render


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

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                reply_to=[email] if email else None,
            )
            return render(request, "home/index.html", {"success": True})
        except Exception:
            return render(
                request,
                "home/index.html",
                {"error": "No se pudo enviar el correo. Intenta nuevamente."},
            )

    return render(request, "home/index.html")
