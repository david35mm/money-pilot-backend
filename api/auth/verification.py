from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import string

from pydantic import EmailStr

from api import config


def generate_verification_code(length: int = 6) -> str:
  """Genera un código de verificación alfanumérico."""
  characters = string.ascii_uppercase + string.digits
  return ''.join(random.choice(characters) for _ in range(length))


# --- Simulación de envío de email ---
def send_verification_email(to_email: EmailStr, code: str):
  """
    Simula el envío de un email de verificación.
    En producción, aquí se integraría con un servicio de email real.
    """
  # Simplemente imprime el código en consola para fines de prueba
  print(
      f"[SIMULACIÓN] Enviando email de verificación a {to_email} con código: {code}"
  )
  # Aquí iría el código real para enviar el email, por ejemplo:
  # server = smtplib.SMTP('smtp.gmail.com', 587)
  # server.starttls()
  # server.login(sender_email, sender_password)
  # msg = MIMEMultipart()
  # msg['From'] = sender_email
  # msg['To'] = to_email
  # msg['Subject'] = "Código de Verificación - MoneyPilot"
  # body = f"Tu código de verificación es: {code}"
  # msg.attach(MIMEText(body, 'plain'))
  # server.send_message(msg)
  # server.quit()
  return True


# --- Simulación de envío de SMS (placeholder) ---
def send_verification_sms(to_phone: str, code: str):
  """
    Placeholder para enviar un SMS de verificación.
    En producción, se integraría con un servicio de SMS.
    """
  print(
      f"[SIMULACIÓN] Enviando SMS de verificación a {to_phone} con código: {code}"
  )
  return True
