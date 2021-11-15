# import json
import os
import socket
import sys
import threading
import time

from FTPServer import FTPServer

NUM_CONN: int = 3
LIST_CONN: list[socket.socket] = []
LIST_THREAD: list[threading.Thread] = []
CONTADOR: int = 0


def cliente(conn: socket.socket, addr: tuple, name: str) -> None:
    global LIST_CONN
    global LIST_THREAD
    with conn as client_conn:
        salir: str = ''
        ftp_server = FTPServer(conn_cli=client_conn, nombre=name)
        if ftp_server.validacion():
            msg_env: str
            msg_rcv: str
            print(f'Acceso concedido a [{ftp_server.nombre}]')
            while salir != 'QUIT':
                archivos = os.listdir(ftp_server.directorio)
                msg_env = 'Lista de Documentos: ' + ', '.join(archivos)
                ftp_server.enviar_mensaje(msg_env)
                msg_rcv = ftp_server.recibir_mensaje()
                ftp_server.transferencia_archivo(msg_rcv)
                msg_rcv = ftp_server.recibir_mensaje()
                if msg_rcv == 'QUIT':
                    print(f'Desconectando a { addr }')
                    break
        else:
            print(f'Acceso denegado a [{ftp_server.nombre}]')
    LIST_CONN.remove(client_conn)
    LIST_THREAD.remove(threading.currentThread())
    print(f'Hilo acabado de { addr }')
    return


def servir_siempre(tcp_socket: socket, _host: str, _port: int) -> None:
    global NUM_CONN
    global LIST_CONN
    global LIST_THREAD
    global CONTADOR
    try:
        while True:
            client_conn, client_addr = tcp_socket.accept()
            print(f'Conectando a: { client_addr }')
            LIST_CONN.append(client_conn)
            CONTADOR += 1
            name_thread: str = f'Conexion-{CONTADOR}'
            client_conn.sendall(str.encode(f'Conectado a [{ _host }:{ _port }]'))
            thread_read = threading.Thread(
                target=cliente,
                name=name_thread,
                args=[client_conn, client_addr, name_thread]
            )
            LIST_THREAD.append(thread_read)
            LIST_CONN.append(client_conn)
            thread_read.start()
    except Exception as _e:
        print(_e)
    finally:
        return


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Comando: python { sys.argv[0] } <PORT> <NUM_CONN>')

    try:
        port = int(sys.argv[1])
        if port < 1024:
            port = 1234

        NUM_CONN = int(sys.argv[2])
        if 3 > NUM_CONN > 100:
            NUM_CONN = 3
    except Exception as e:
        print(e)
        print(f'Comando: python {sys.argv[0]} <PORT: int> <NUM_CONN: int>')
        sys.exit(1)

    print('Iniciando Servidor FTP'.center(100, '-'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        host = socket.gethostbyname(socket.gethostname())
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind((host, port))
        TCPServerSocket.listen(NUM_CONN)
        print(f'El servidor TCP [{host}:{port}] está disponible...')
        servir_siempre(TCPServerSocket, host, port)
    print('Terminando Servidor FTP'.center(100, '-'))
