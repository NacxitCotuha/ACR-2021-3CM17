import socket
import os
import sys
import time


class ClienteVoz:
    def __init__(self, conn: socket.socket) -> None:
        self._conn: socket.socket = conn
        self._bufferSize: int = 1024
        return

    def recibir_mensaje(self) -> str:
        aux: bytes = b''
        while aux == b'':
            aux = self._conn.recv(self._bufferSize)
        mensaje: str = aux.decode('utf-8')
        return mensaje

    def enviar_mensaje(self, msg: str) -> None:
        aux: bytes = str.encode(msg)
        self._conn.sendall(aux)
        print(f'Mensaje enviado a servidor: {msg}')
        return


def conectar_servidor_voz():
    try:
        host: str = str(sys.argv[1])
        port: int = int(sys.argv[2])
        msg_rcv: str
        msg_env: str
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerVoz:
            TCPServerVoz.connect((host, port))
            conn_servidor: ClienteVoz = ClienteVoz(conn=TCPServerVoz)
            msg_rcv = conn_servidor.recibir_mensaje()
            if '[SETTING]' in msg_rcv:
                

    except ValueError:
        print(f'Usage: {sys.argv[0]} <HOST: str> <PORT: int>')
        sys.exit(1)


def main() -> None:
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <HOST> <PORT>')
        sys.exit(1)
    conectar_servidor_voz()
    return


if __name__ == '__main__':
    main()
