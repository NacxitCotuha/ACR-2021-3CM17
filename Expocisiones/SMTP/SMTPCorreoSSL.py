import smtplib
import ssl

# Estas importaciones es para dar cuerpo al correo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = 465  # Es un puerto de segurida que usa SSL
PASSWORD = 'passwordPerron'
SMTP_GMAIL = 'smtp.gmail.com'
CORREO = 'pruebasc121@gmail.com'
HTML = '''
<html>
  <body>
    <p>Hola,<br>
       Mira mas ejemplos en:<br>
       <a href="http://www.realpython.com">Real Python</a> 
    </p>
  </body>
</html>
'''


def prompt(_prompt) -> str:
    return input(_prompt).strip()  # Elimina los espacios del input


def cuerpo_correo(_destino) -> str:
    global HTML
    __mensaje = MIMEMultipart('alternative')
    __mensaje['From'] = CORREO  # Tu direccion de correo
    __mensaje['To'] = _destino  # Direccion correo destino
    __mensaje['Subject'] = 'Subscription'  # Asunto del correo
    # Turn these into plain/html MIMEText objects
    __part = MIMEText(HTML, "html")

    # Add HTML to MIMEMultipart message
    # The email client will try to render the last part first
    __mensaje.attach(__part)
    # __mensaje.attach(__part1)
    return __mensaje.as_string()


if __name__ == '__main__':
    # Crear contexto de seguridad SSL
    destino = prompt('Inserte correo destino: ')
    context = ssl.create_default_context()
    mensaje = cuerpo_correo(destino)
    with smtplib.SMTP_SSL(SMTP_GMAIL, PORT, context=context) as server:
        server.login(CORREO, PASSWORD)
        server.sendmail(CORREO, destino, mensaje)
