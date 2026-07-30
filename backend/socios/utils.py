import os
import requests
import logging

logger = logging.getLogger(__name__)

def enviar_notificacion_telegram(nombre_socio, telefono_socio):
    # Poné el token y el chat_id en variables de entorno para no dejarlos en el código.
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    
    if not TOKEN or not CHAT_ID:
        logger.error("Telegram token o chat ID no configurados.")
        print("[Telegram] token o chat ID no configurados.")
        return

    mensaje = f"🔔 *¡Nuevo Socio Registrado!*\n\n👤 *Nombre:* {nombre_socio}\n📞 *Teléfono:* {telefono_socio}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload = {
        'chat_id': CHAT_ID,
        'text': mensaje,
        'parse_mode': 'Markdown' # Permite que el texto tenga negritas
    }
    
    print(f"[Telegram] enviando mensaje a chat {CHAT_ID}")
    try:
        response = requests.post(url, data=payload)
        print(f"[Telegram] status={response.status_code} text={response.text}")
        if response.status_code != 200:
            logger.error(f"Error al enviar mensaje a Telegram: {response.text}")
    except Exception as e:
        logger.error(f"Error de conexión con Telegram: {str(e)}")
        print(f"[Telegram] excepción: {str(e)}")


def enviar_notificacion_instagram(nombre_socio, telefono_socio):
    """Placeholder for Instagram notification.

    Actualmente la aplicación usa un webhook o servicio externo para notificaciones.
    Ajustá esta función cuando tengas la API de Instagram / Meta disponible.
    """
    logger.info(
        f"Enviar notificación de Instagram: socio={nombre_socio}, telefono={telefono_socio}"
    )
    # Ejemplo: aquí podrías usar requests.post() con tu endpoint de notificaciones.
