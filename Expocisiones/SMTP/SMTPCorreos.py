# Importacion de paquetes necesarios
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def prompt(_prompt) -> str:
    return input(_prompt).strip()  # Elimina los espacios del input


if __name__ == '__main__':
    # Instancia del objeto correo
    correo = MIMEMultipart()

    # Mensaje a enviar
    mensaje = input('Escribir mensaje: ')

    # Configurar los parametros del correo
    password = 'passwordPerron'
    correo['From'] = 'pruebasc121@gmail.com'  # Tu direccion de correo
    correo['To'] = 'nacxit.cotuha@gmail.com'  # Direccion correo destino
    correo['Subject'] = 'Subscription'  # Asunto del correo

    # Agregar cuerpo del correo
    correo.attach(MIMEText(mensaje, 'plain'))

    # Crear server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    # Login Credentials for sending the mail
    server.login(correo['From'], password)

    # enviar el mensaje por el server
    server.sendmail(correo['From'], correo['To'], correo.as_string())

    server.quit()

    print(f'Successfully sent email to {correo["To"]}')
