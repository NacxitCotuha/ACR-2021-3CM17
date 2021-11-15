import json
import os
import socket
import struct
# import time


class ServerFile:
    def __init__(self, directory: str, host: str, port: int, conn: socket.socket) -> None:
        self._directory: str = directory
        self._host: str = host
        self._port: int = port
        self._conn: socket.socket = conn
        print(f'Conexion Iniciada para transferencia en <{ self._host }:{ self._port }>')
        return

    def mandar_archivo(self) -> None:
        # Obtener el tamaño del archivo a enviar
        filesize = os.path.getsize(self._directory)
        # Informar primero al servidor la cantidad
        # de bytes que serán enviados.
        self._conn.sendall(struct.pack('<Q', filesize))
        with open(self._directory, "rb") as f:
            while read_bytes := f.read(1024):
                self._conn.sendall(read_bytes)
        return


class FTPServer:
    PORT: int = 1
    NUM_CONN: int = 3

    def __init__(self, conn_cli: socket.socket, nombre: str) -> None:
        self._conn: socket.socket = conn_cli  # Conexion del cliente con el servidor
        self._nombre: str = nombre  # Nombre de la conexion y hilo que se
        self._directorio: str = ''  # Directorio que se va a manejar
        return

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def directorio(self) -> str:
        return self._directorio

    # Enviar - Recibir mensajes
    def enviar_mensaje(self, msg: str) -> None:
        print(f'Mensaje Enviado a  [{self._nombre}]: "{msg}"')
        aux: bytes = str.encode(msg)
        self._conn.sendall(aux)
        return

    def recibir_mensaje(self) -> str:
        aux: bytes = b''
        while aux == b'':
            aux = self._conn.recv(1024)
        msg: str = aux.decode('utf-8')
        print(f'Mensaje Recibido de [{ self._nombre }]: "{ msg }"')
        return msg

    def validacion(self) -> bool:
        self.enviar_mensaje('Ingrese Nombre de Usuario: ')
        username: str = self.recibir_mensaje()
        self.enviar_mensaje('Ingrese Password: ')
        password: str = self.recibir_mensaje()
        with open('users.json') as file:
            file_json = json.load(file)
            for usuario in file_json['usuarios']:
                if (username == usuario['username']) and (password == usuario['password']):
                    self.enviar_mensaje('ACEPTADO')
                    self._directorio = usuario['directorio']
                    print(f'Directorio de [{ self._nombre }]: "{ self._directorio }')
                    return True
            else:
                self.enviar_mensaje('DENEGADO')
                return False

    def transferencia_archivo(self, filename: str):
        host: str = self.recibir_mensaje()
        port: int = int(self.recibir_mensaje())
        directorio: str = self._directorio + filename
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerFile:
            TCPServerFile.connect((host, port))
            print('Conexion e')
            file_client: ServerFile = ServerFile(directorio, host, port, TCPServerFile)
            file_client.mandar_archivo()
        print(f'Archivo enviado : { directorio } ')
        return


if __name__ == '__main__':
    print('FTP Servidor Prueba'.center(100, '-'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        hname = socket.gethostbyname(socket.gethostname())
        hport = 8888
        TCPServerSocket.bind((hname, hport))
        TCPServerSocket.listen()
        print(f'El servidor TCP [{ hname }:{ hport }] está disponible...')
        client_conn, client_addr = TCPServerSocket.accept()
        with client_conn:
            msg_env: str = ''
            msg_rcv: str = ''
            ftp_server = FTPServer(conn_cli=client_conn, nombre='Conexion')
            ftp_server.enviar_mensaje(f'Se ha conextado a { hname }:{ hport }')
            if ftp_server.validacion():
                print(f'Acceso concedido a [{ ftp_server.nombre }]')
                archivos = os.listdir(ftp_server.directorio)
                msg_env = 'Lista de Documentos: ' + ', '.join(archivos)
                ftp_server.enviar_mensaje(msg_env)
                msg_rcv = ftp_server.recibir_mensaje()
                ftp_server.transferencia_archivo(msg_rcv)
            else:
                print(f'Acceso denegado a [{ ftp_server.nombre }]')
    print('FTPServidor Pruebas Terminadas'.center(100, '-'))
