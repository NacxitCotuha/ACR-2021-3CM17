import threading
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)


def daemon():
    logging.debug('Iniciando')
    time.sleep(2)
    logging.debug('Terminando')


def non_daemon():
    logging.debug('Iniciado')
    logging.debug('Terminado')


d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()
logging.debug('Hilo demonio e hilo normal iniciados')
d.join()

# d.join()
# t.join()
