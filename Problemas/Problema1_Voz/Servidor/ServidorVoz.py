import logging
import threading
import time
import socket
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',
)


def get_host() -> str:
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host_ip: str
    try:
        st.connect(('10.255.255.255', 1))
        host_ip = st.getsockname()[0]
    except ConnectionError:
        host_ip = '127.0.0.1'
    finally:
        st.close()
    return host_ip


class ActivePool:
    def __init__(self):
        super(ActivePool, self).__init__()
        self._active = []
        self._lock = threading.Lock()

    def make_active(self, name):
        self._active.append(name)
        logging.debug(f'Ejecutando: {self._active}')

    def make_inactive(self, name):
        with self._lock:
            self._active.remove(name)
            logging.debug(f'Terminando Turno: {self._active}')


class ServidorConfiguracion:
    def __init__(self, client_conn: socket.socket, client_addr: socket.socket):
        self._conn = client_conn
        self._addr = client_addr
        self._bufferSize = 1024
        return

    def enviar_mensaje(self, mensaje: str) -> None:
        aux: bytes = str.encode(mensaje)
        self._conn.sendall(aux)
        print(f'Mensaje enviado a [{self._addr}]')
        return

    def recibir_mensaje(self) -> str:
        aux: bytes = b''
        while aux == b'':
            aux = self._conn.recv(self._bufferSize)
        mensaje: str = aux.decode('utf-8')
        return mensaje


class ServidorJuego:
    def __init__(self):
        self._listConn: list[socket.socket] = []
        self._bufferSize: int = 1024
        self._conectados: int = 0
        self._statusGame: bool = True

    @property
    def status_game(self) -> bool:
        return self._statusGame

    @property
    def conectados(self) -> int:
        return self._conectados

    def agregar_conexion(self, conn: socket.socket):
        self._listConn.append(conn)
        self._conectados += 1
        return

    def gestionar_conexiones(self):
        for conn in self._listConn:
            if conn.fileno() == -1:
                self._listConn.remove(conn)
                self._conectados -= 1
        print(f'Hilos activos: {threading.active_count()}')
        # print(f'Enum: {threading.enumerate()}')
        print(f'Conexiones: {len(self._listConn)}')
        # print(self._listConn)
        return

    @staticmethod
    def enviar_mensaje(conn: socket.socket, addr: socket.socket, msg: str) -> None:
        aux: bytes = str.encode(msg)
        conn.sendall(aux)
        print(f'[{addr}] recibira: {msg}')
        return

    def recibir_mensaje(self, conn: socket.socket, addr: socket.socket) -> str:
        aux: bytes = b''
        while aux == b'':
            aux = conn.recv(self._bufferSize)
        mensaje: str = aux.decode('utf-8')
        print(f'[{addr}] envio: {mensaje}')
        return mensaje

    def enviar_mensaje_todos(self, msg: str, conn_except: socket.socket or str, name_except: str):
        aux: bytes = str.encode(msg)
        for conn in self._listConn:
            if conn != conn_except:
                conn.sendall(aux)
        if conn_except == '':
            print(f'Mensaje enviado a todos sin excepcion')
        else:
            print(f'Mensaje enviado a todos excepto: {name_except}')
        return


JUEGO: ServidorJuego  # Variable Global


def jugador_thread(conn: socket.socket, addr: socket.socket, s: threading.Semaphore, pool: ActivePool) -> None:
    try:
        global JUEGO
        msg_rcv: str
        msg_env: str
        jugador: str = threading.currentThread().getName()
        logging.debug(f'[{jugador}] se ha conectado.')
        while JUEGO.status_game:
            with s:
                pool.make_active(jugador)
                if JUEGO.status_game:
                    pass

    except Exception as e:
        print(e)
    finally:
        print(f'[{addr}] finalizo la conexion...')
        conn.close()
        time.sleep(10)
    return


def servidor_juego(host: str, port: int, no_jugadores: int) -> None:
    global JUEGO
    list_thread: list[threading.Thread] = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerJuego:
        TCPServerJuego.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerJuego.bind((host, port))
        TCPServerJuego.listen(no_jugadores)
        print(f'Servidor de Juego [{host}:{port}]esta a la espera de los jugador(es)')
        try:
            JUEGO: ServidorJuego = ServidorJuego()
            pool = ActivePool()
            s = threading.Semaphore()
            while JUEGO.status_game:
                client_conn, client_addr = TCPServerJuego.accept()
                print(f'Conectando a {client_addr}...')
                JUEGO.agregar_conexion(conn=client_conn)
                name_thread = f'Jugador-{JUEGO.conectados}'
                JUEGO.enviar_mensaje(conn=client_conn, addr=client_addr, msg=name_thread)
                thread_read = threading.Thread(
                    target=jugador_thread,
                    name=name_thread,
                    args=[client_conn, client_addr, s, pool]
                )
                list_thread.append(thread_read)
                if JUEGO.conectados == no_jugadores:
                    for hilo in list_thread:
                        hilo.start()
                        time.sleep(0.5)
                else:
                    JUEGO.enviar_mensaje_todos(
                        msg='[WAIT] Espera a que se unan mas jugadores',
                        conn_except='',
                        name_except='')
                JUEGO.gestionar_conexiones()
        except Exception as e:
            print(e)
    return


def servidor_configuracion():
    host: str = get_host()
    port: int = 8080
    mensaje: str
    no_jugadores: int
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerConfig:
        TCPServerConfig.bind((host, port))
        TCPServerConfig.listen()
        print(f'Servidor [{host}:{port}] de configuracion a la espera de un jugador...')
        client_conn, client_addr = TCPServerConfig.accept()
        with client_conn:
            print(f'Conectando a {client_addr}')
            client: ServidorConfiguracion = ServidorConfiguracion(client_conn=client_conn, client_addr=client_addr)
            client.enviar_mensaje(
                '[SETTING] Te has conectado al Servidor, favor de poner el numero de participantes a jugar: '
            )
            mensaje = client.recibir_mensaje()
            no_jugadores = int(mensaje)
            while no_jugadores < 1:
                client.enviar_mensaje('[Error] numero de juagores no valido ingreselo de nuevo: ')
                mensaje = client.recibir_mensaje()
                no_jugadores = int(mensaje)
            client.enviar_mensaje(f'Reconfigurando el servidor para el acceso de [{no_jugadores}] jugadores...')
    servidor_juego(host=host, port=port, no_jugadores=no_jugadores)
    return


def main() -> None:
    servidor_configuracion()
    return


if __name__ == '__main__':
    print('Servidor de Voz'.center(100, '-'))
    main()
