import logging
import threading
import time

# Agregar el buffer finito (10 elementos)
# Agregar condición de parada del productor
# Agregar condición de consumo
# Agregar producción y el consumo (manipulación de buffer)

buffer = []

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',
)


def consumer(_mutex):
    global buffer

    logging.debug('Iniciando hilo consumidor')
    # t = threading.currentThread()
    while 1:
        with _mutex:
            logging.debug('Espereando Recurso')
            mutex.wait()
            print(buffer)
            buffer.remove('Producto')
            logging.debug('removi un recurso')
        time.sleep(1)


def producer(_mutex, _max_produccion):
    global buffer
    """set up the resource to be used by the consumer"""
    logging.debug('Iniciando el hilo productor')
    while 1:
        with _max_produccion:
            if len(buffer) < 10:
                _max_produccion.notify()
                logging.debug('empiezen a producir')
                with _mutex:
                    logging.debug('produciendo')
                    buffer.append('Producto')
                    logging.debug('Poniendo los recursos disponibles')
                    _mutex.notifyAll()
            else:
                logging.debug('Detniendo Produccion')
                _max_produccion.wait()
        time.sleep(1)


mutex = threading.Condition()
conditionProduccionMax = threading.Condition()

c1 = threading.Thread(name='c1', target=consumer, args=(mutex,))
c2 = threading.Thread(name='c2', target=consumer, args=(mutex,))
p1 = threading.Thread(name='p1', target=producer, args=(mutex, conditionProduccionMax))
p2 = threading.Thread(name='p2', target=producer, args=(mutex, conditionProduccionMax))

c1.start()
c2.start()
p1.start()
p2.start()
