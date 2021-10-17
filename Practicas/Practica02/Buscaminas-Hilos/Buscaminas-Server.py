from Buscaminas import Buscaminas
from ConnSocket import ConnSocket

import logging
import time
import threading
import socket
import sys

listConn: list = []
listThread: list = []
statusGame: bool = True
juego = None
conectados: int = 0
NUM_CONNS: int
dificultadStr: str
tiempoInicio: float
# Significado de Flags
# Enviar 0: Mensaje de GAME OVER a todos los usuarios
# Enviar 1: el cliente estara solo para recibir mensajes solamente
# Enviar 2: El cliente entra en modo jugador osea es su turno
# Enviar 3: Poner a la espera todos los usuarios-cliente

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',
)


class ActivePool:
    def __init__(self):
        super(ActivePool, self).__init__()
        self.__active = []
        self.__lock = threading.Lock()

    def make_active(self, _name):
        self.__active.append(_name)
        logging.debug(f'Ejecutando: {self.__active}')

    def make_inactive(self, _name):
        with self.__lock:
            self.__active.remove(_name)
            logging.debug(f'Terminando Turno: {self.__active}')


def enviar_everyone(_exception_name: str, _conn, _mensaje: str):
    global listConn
    __msg_env = str.encode(_mensaje)

    for __conn in listConn:
        if _conn != __conn:
            __conn.sendall(__msg_env)

    if _exception_name != '':
        print(f'Enviado a todos excepto {_exception_name}')
    else:
        print(f'Enviado a tdos sin excepcion')


def enviar_flag_everyone(_exception_name: str, _conn, _flag: int):
    global listConn
    __flag_env = str.encode(str(_flag))

    for __conn in listConn:
        if _conn != __conn:
            __conn.sendall(__flag_env)

    if _exception_name != '':
        print(f'Enviado a todos excepto {_exception_name}')
    else:
        print(f'Enviado a tdos sin excepcion')


def cliente(_conn, _addr, _s, _pool):
    try:
        msg_env: str
        msg_rcv: str
        __coor_x: int
        __coor_y: int
        global juego
        global statusGame
        global conectados
        global dificultadStr
        __jugador: str = threading.currentThread().getName()
        logging.debug(f'{__jugador} conectado...')
        __conn_s = ConnSocket(_conn, __jugador)
        __tu_turno: bool = True
        while statusGame:
            with _s:
                _pool.make_active(__jugador)
                __tu_turno = True
                if statusGame:
                    enviar_flag_everyone(__jugador, _conn, 1)
                    msg_env = f'Dificultad: {dificultadStr}\n'
                    msg_env += juego.imprimir_mapa() + '\n'
                    __conn_s.enviar_flag(2)
                    enviar_everyone(__jugador, _conn, msg_env + f'Turno de: {__jugador}')
                    msg_env += 'Es tu turno \n'
                    msg_env += 'Inserte las coordenadas (x,y) -> (columna, fila):\n'
                    msg_env += 'Columna - Eje X(int):\n'
                    __conn_s.enviar(msg_env)
                    # Recibimos el eje X
                    msg_rcv = __conn_s.recibir()
                    __coor_x = int(msg_rcv)
                    # Recibimos el Eje Y
                    msg_env = 'Fila - Eje Y(int): \n'
                    __conn_s.enviar(msg_env)
                    msg_rcv = __conn_s.recibir()
                    __coor_y = int(msg_rcv)
                    # ERROR de Coordenadas
                    while not juego.in_coor(__coor_x, __coor_y):
                        __conn_s.enviar('error')
                        msg_env = 'Coordenadas Incorrectas intentelo otra vez \n'
                        msg_env += 'Columna - Eje X(int):\n'
                        __conn_s.enviar(msg_env)
                        # Recibimos el eje X
                        msg_rcv = __conn_s.recibir()
                        __coor_x = int(msg_rcv)
                        # Recibimos el Eje Y
                        msg_env = 'Fila - Eje Y(int): \n'
                        __conn_s.enviar(msg_env)
                        msg_rcv = __conn_s.recibir()
                        __coor_y = int(msg_rcv)
                    else:
                        __conn_s.enviar('accept')
                        time.sleep(0.5)
                        if juego.jugar_new_coor():
                            if juego.state_juego():
                                enviar_flag_everyone('', 0, 0)  # Enviar a todos sin excepcion
                                tiempo_final = time.time()
                                msg_env = 'HAN GANADO\n'
                                msg_env += juego.imprimir_mapa() + '\n'
                                msg_env += f'Puntuacion Total: {juego.puntaje}\n'
                                msg_env += f'Tiempo total de la partida: {(tiempo_final - tiempoInicio): .2f}'
                                enviar_everyone('', 0, msg_env)
                                statusGame = False

                            else:
                                enviar_flag_everyone('', 0, 1)  # Enviar a todos sin excepcion
                                msg_env = juego.imprimir_mapa() + '\n'
                                msg_env += f'Puntuacion Actual: {juego.puntaje}\n'
                                msg_env += f'El turno de {__jugador} ha terminado'
                                enviar_everyone('', 0, msg_env)
                                statusGame = True
                                time.sleep(2)
                        else:
                            enviar_flag_everyone('', 0, 0)  # Enviar a todos sin excepcion
                            tiempo_final = time.time()
                            msg_env = 'HAN PERDIDO\n'
                            msg_env += juego.imprimir_mapa() + '\n'
                            msg_env += f'Puntuacion Total: {juego.puntaje}\n'
                            msg_env += f'Tiempo total de la partida: {(tiempo_final - tiempoInicio): .2f}'
                            enviar_everyone('', 0, msg_env)
                            statusGame = False
                _pool.make_inactive(__jugador)
            time.sleep(0.5)

    except Exception as e:
        print(e)

    finally:
        print(f'Fin de la conexion')
        _conn.close()
        time.sleep(10)
        sys.exit(0)


def gestionar_conexiones():
    global listConn
    global listThread
    global conectados
    global statusGame

    for __conn in listConn:
        if __conn.fileno() == -1:
            listConn.remove(__conn)
            conectados -= 1

    print(f'Hilos activos: {threading.active_count()}')
    # print(f'Enum: {threading.enumerate()}')
    print(f'Conexiones: {len(listConn)}')
    print(listConn)


def servidor_esclavo(_tcp_server_socket):
    try:
        global listConn
        global conectados
        global NUM_CONNS
        global tiempoInicio
        global statusGame
        __pool = ActivePool()
        __s = threading.Semaphore()

        while statusGame:
            __client_conn, __client_addr = _tcp_server_socket.accept()
            print(f'Conectando a {__client_addr}')
            listConn.append(__client_conn)
            conectados += 1
            __name_thread = f'Jugador-{conectados}'
            __client_conn.sendall(str.encode(__name_thread))
            __thread_read = threading.Thread(
                target=cliente,
                name=__name_thread,
                args=[__client_conn, __client_addr, __s, __pool]
            )
            listThread.append(__thread_read)

            if conectados == NUM_CONNS:
                __aux: float = 0
                tiempoInicio = time.time()
                for hilo in listThread:
                    hilo.start()
                    time.sleep(__aux)
                    __aux += 0.5

            else:
                enviar_flag_everyone('los que no se han conectado', 0, 3)

            gestionar_conexiones()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        # print(f'Usage: {sys.argv[0]} <host> <port> <num_connections>')
        print(f'Usage: {sys.argv[0]} <HOST> <PORT> <num_connections> <dificultad = 1 | 2 (principiante | Avanzado)>')
        sys.exit(1)

    HOST: str = str(sys.argv[1])
    PORT: int = int(sys.argv[2])
    NUM_CONNS = int(sys.argv[3])

    if sys.argv[4] == '1' or sys.argv[4] == '2':
        DIFICULTAD = int(sys.argv[4])
    else:
        print(f'Usage: {sys.argv[0]} <HOST> <PORT> <num_connections> <dificultad = 1 | 2 (principiante | Avanzado)>')
        sys.exit(1)

    if 0 <= DIFICULTAD <= 2:
        juego = Buscaminas(DIFICULTAD)
    else:
        print(f'Usage: {sys.argv[0]} <HOST> <PORT> <num_connections> <dificultad = 1 | 2 (principiante | Avanzado)>')
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind((HOST, PORT))
        TCPServerSocket.listen(NUM_CONNS)
        print("El servidor TCP está disponible y en espera de solicitudes")

        if juego.dificultad() == 1:
            dificultadStr = 'Principiante'

        elif juego.dificultad() == 2:
            dificultadStr = 'Avanzado'

        servidor_esclavo(TCPServerSocket)
        time.sleep(2)
        print('Fin del juego todos los clientes han sido desconectados')
