import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PORT = 465  # Es un puerto de segurida que usa SSL
SMTP_GMAIL = 'smtp.gmail.com'

subject_email = 'Correo con PDF'
body_email = 'Este correo fue enviado desde un programa en python'
send_email = 'pruebasc121@gmail.com'
password_email = 'passwordPerron'

recv_email: str


def prompt(_prompt):
    return input(_prompt).strip()


def multipart_message() -> str:
    global send_email
    global recv_email
    global body_email
    global subject_email
    __message = MIMEMultipart()
    __message['From'] = send_email
    __message['To'] = recv_email
    __message['Subject'] = subject_email
    __message['Bcc'] = recv_email  # Recomendado para correos masivos

    # Agregar cuerpo al correo
    __message.attach(MIMEText(body_email, 'plain'))

    # Abrir Archivo PDF en modo binario
    __filename = 'Practica2.pdf'
    with open(__filename, 'rb') as attachment:
        # Agregar archivo como application/octet-stream
        # Email client can usually download this automatically as attachment
        __part = MIMEBase('application', 'octet-stream')
        __part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(__part)

        # Add header as key/value pair to attachment part
        __part.add_header(
            "Content-Disposition",
            f"attachment; filename= {__filename}",
        )

        # Add attachment to message and convert message to string
        __message.attach(__part)
        return __message.as_string()


if __name__ == '__main__':
    recv_email = prompt('Inserte Correo destino: ')
    mensaje = multipart_message()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_GMAIL, PORT, context=context) as server:
        server.login(send_email, password_email)
        server.sendmail(send_email, recv_email, mensaje)
