# Despliegue de IA Tech → iatechcorp.com (Railway + Cloudflare)

Guía paso a paso. El código ya está listo (Gunicorn + WhiteNoise + Procfile).

---

## 1. Subir el código a GitHub

Railway despliega desde un repo de GitHub.

```bash
git add .
git commit -m "Configuración de producción (Railway + WhiteNoise + Gunicorn)"
git push
```

Si aún no tienes el repo en GitHub, créalo en github.com y sigue las
instrucciones de `git remote add origin ...`.

---

## 2. Crear el proyecto en Railway

1. Entra a https://railway.app y haz login con GitHub.
2. **New Project → Deploy from GitHub repo →** elige este repositorio.
3. Railway detecta Python por `requirements.txt` y usa el `Procfile`:
   - `release:` corre las migraciones.
   - `web:` arranca Gunicorn.

---

## 3. Variables de entorno en Railway

En el servicio → pestaña **Variables**, agrega (copia de `.env.production.example`):

| Variable | Valor |
|---|---|
| `DEBUG` | `False` |
| `SECRET_KEY` | (la clave larga generada) |
| `ALLOWED_HOSTS` | `iatechcorp.com,www.iatechcorp.com,.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://iatechcorp.com,https://www.iatechcorp.com` |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `true` |
| `EMAIL_HOST_USER` | `iatechcol1006@gmail.com` |
| `EMAIL_HOST_PASSWORD` | (App Password de Gmail, ver paso 5) |
| `DEFAULT_FROM_EMAIL` | `iatechcol1006@gmail.com` |
| `CONTACT_EMAIL` | `contacto@iatechcorp.com` |

Railway redesplegará solo. Cuando termine, te da una URL tipo
`https://iatech-production-xxxx.up.railway.app`. Ábrela: la página debe verse bien.

---

## 4. Conectar el dominio iatechcorp.com (Cloudflare)

1. En Railway → servicio → **Settings → Networking → Custom Domain**.
   Agrega `iatechcorp.com` y `www.iatechcorp.com`. Railway te dará un destino
   tipo `xxxx.up.railway.app` para cada uno.
2. En **Cloudflare → tu dominio → DNS → Records**, crea:
   - Tipo **CNAME**, Name `@` (o `iatechcorp.com`), Target = el destino de Railway, Proxy: **DNS only (nube gris)** al inicio.
   - Tipo **CNAME**, Name `www`, Target = el destino de Railway, Proxy: DNS only.
3. Espera unos minutos. Railway emitirá el certificado HTTPS automáticamente.
4. (Opcional) En Cloudflare → SSL/TLS, modo **Full (strict)**. No uses "Flexible".

> Si Cloudflare no deja un CNAME en la raíz `@`, activa "CNAME flattening"
> (Cloudflare lo hace solo) o usa un registro A con la IP que indique Railway.

---

## 5. Gmail App Password (para enviar el correo)

El SMTP de Gmail NO acepta tu contraseña normal; necesita un "App Password".

1. La cuenta `iatechcol1006@gmail.com` debe tener **verificación en 2 pasos** activada.
   (myaccount.google.com → Seguridad → Verificación en 2 pasos).
2. Luego ve a https://myaccount.google.com/apppasswords
3. Crea una contraseña de aplicación (nombre: "IA Tech web"). Te da 16 letras.
4. Pega esas 16 letras (sin espacios) en `EMAIL_HOST_PASSWORD` en Railway.

---

## 6. Correo contacto@iatechcorp.com (Cloudflare Email Routing — gratis)

Para que los mensajes te lleguen a una dirección con tu dominio:

1. Cloudflare → tu dominio → **Email → Email Routing → Enable**.
2. Cloudflare agrega solo los registros MX necesarios.
3. En **Routing rules**, crea: `contacto@iatechcorp.com` → reenviar a
   `iatechcol1006@gmail.com` (confirma el reenvío desde tu Gmail).

Listo: el formulario envía a `contacto@iatechcorp.com` y tú lo recibes en tu Gmail.

> Nota: aquí el correo se ENVÍA desde tu Gmail (paso 5) y se RECIBE en
> contacto@iatechcorp.com (este paso). Son cosas distintas y ambas se necesitan.

---

## 7. Probar

1. Abre https://iatechcorp.com
2. Llena el formulario de contacto y envía.
3. Revisa que llegue el correo a tu Gmail.

¡Listo! 🚀

---

## Notas

- La base de datos es SQLite y en Railway el disco se reinicia en cada
  despliegue. Para esta página no importa (no guarda datos; el formulario solo
  manda correos). Si algún día agregas login/admin persistente, añade un
  volumen en Railway o cambia a PostgreSQL.
