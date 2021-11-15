import threading
import smtpd
import asyncore
import smtplib

import email.utils
from email.mime.text import MIMEText

# server = smtpd.SMTPServer(('localhost', 1025), None)
loop_thread = threading.Thread(target=asyncore.loop, name="Asyncore Loop")
# If you want to make the thread a daemon
# loop_thread.daemon = True
loop_thread.start()

# port should match your SMTP server
client = smtplib.SMTP('localhost', port=1025)
# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'recipient@example.com'))
msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
msg['Subject'] = 'Simple test message'
client.set_debuglevel(True)
try:
    client.sendmail(msg['From'], msg['To'], msg)
finally:
    client.quit()
