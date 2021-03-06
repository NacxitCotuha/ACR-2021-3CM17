import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )
class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Ejecutando: %s', self.active)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Ejecutando: %s', self.active)

def worker(s, pool):
    logging.debug('Esperando para acceder al grupo/parque/agrupación/reserva')
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        time.sleep(2)
        pool.makeInactive(name)

pool = ActivePool()
s = threading.Semaphore(2)
for i in range(100):
    t = threading.Thread(target=worker, name=str(i), args=(s, pool))
    t.start()