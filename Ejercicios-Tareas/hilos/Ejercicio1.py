import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


def factorial(numero: int) -> int:
    if numero > 1:
        numero = numero * factorial(numero - 1)
        time.sleep(0.5)
    return numero


def tarea_hilo(noHilo: int, numero: int):
    logging.debug('Iniciando')
    fact = factorial(numero)
    print(f'Hilo [{noHilo}], su factorial es: {fact}')
    logging.debug('terminado')


noHilos = int(input('Ingrese el numero de hilos a crear(int):'))
hilos: list = []


for hilo in range(noHilos):
    calcFact = int(input(f'Ingrese el Factorial a calcular para el hilo-{hilo + 1}:'))
    t = threading.Thread(name=f'Hilo-{hilo + 1}', target=tarea_hilo, args=(hilo, calcFact,))
    if hilo == 0:
        hilos.insert(0, t)
    else:
        hilos.append(t)

for hilo in range(noHilos):
    hilos[hilo].start()
    hilos[hilo].join()


hilos.clear()
del hilos
