import socket
import struct
import time


def prompt(msg: str) -> str:
    return input(msg).strip()


def in_data(msg: str) -> str:
    return str(input(msg))


class ClientFile:
    def __init__(self, conn: socket.socket, addr: tuple, filename: str) -> None:
        self._conn: socket.socket = conn
        self._addr: tuple = addr
        self._filename: str = filename
        return

    def _recibir_tam_arch(self) -> int:
        # Esta función se asegura de que se reciban los bytes
        # que indican el tamaño del archivo que será enviado,
        # que es codificado por el cliente vía struct.pack(),
        # función la cual genera una secuencia de bytes que
        # representan el tamaño del archivo.
        fmt = '<Q'
        expected_bytes: int = struct.calcsize(fmt)
        received_bytes: int = 0
        stream = bytes()
        while received_bytes < expected_bytes:
            chunk: bytes = self._conn.recv(expected_bytes - received_bytes)
            stream += chunk
            received_bytes += len(chunk)
        tam_arch: int = struct.unpack(fmt, stream)[0]
        return tam_arch

    def recibir_archivo(self) -> None:
        # Leer primero del socket la cantidad de
        # bytes que se recibirán del archivo
        print(f'Recibiendo el archivo: { self._filename }')
        tam_arch: int = self._recibir_tam_arch()
        # Abrir un nuevo archivo en donde guardar
        # los datos recibidos.
        with open('Descargas/' + self._filename, 'wb') as archivo:
            received_bytes = 0
            # Recibir los datos del archivo en bloques de
            # 1024 bytes hasta llegar a la cantidad de
            # bytes total informada por el cliente.
            while received_bytes < tam_arch:
                chunk = self._conn.recv(1024)
                if chunk:
                    archivo.write(chunk)
                    received_bytes += len(chunk)
        return


class FTPClient:
    def __init__(self, conn_serv: socket.socket, nombre: str) -> None:
        self._conn_serv: socket.socket = conn_serv
        self._nombre: str = nombre
        return

    @property
    def nombre(self) -> str:
        return self._nombre

    # Enviar - Recibir mensajes
    def enviar_menssaje(self, msg: str) -> None:
        aux: bytes = str.encode(msg)
        print(f'Mensaje enviado a [{ self._nombre }]: "{ msg }"')
        self._conn_serv.sendall(aux)
        return

    def recibir_mensajes(self) -> str:
        aux: bytes = b''
        while aux == b'':
            aux = self._conn_serv.recv(1024)
        msg: str = str(aux.decode('utf-8'))
        print(f'Mensaje recibido de [{ self._nombre }]: { msg }')
        return msg

    def validacion(self) -> bool:
        msg_r: str = self.recibir_mensajes()
        username: str = prompt(msg_r)
        self.enviar_menssaje(username)
        msg_r = self.recibir_mensajes()
        password: str = prompt(msg_r)
        self.enviar_menssaje(password)
        msg_r = self.recibir_mensajes()
        if msg_r == 'ACEPTADO':
            return True
        else:
            return False

    def transferencia_archivo(self, filename: str, port_transfer: int) -> None:
        host: str = socket.gethostbyname(socket.gethostname())
        self.enviar_menssaje(host)
        time.sleep(0.5)
        self.enviar_menssaje(str(port_transfer))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientArchivo:
            TCPClientArchivo.bind((host, port_transfer))
            TCPClientArchivo.listen()
            print(f'Canal de envio activa en [{ host }:{ port_transfer }] y en espera del archivo')
            server_conn, server_addr = TCPClientArchivo.accept()
            with server_conn:
                file_server: ClientFile = ClientFile(server_conn, server_addr, filename)
                file_server.recibir_archivo()
                print(f'Archivo recibido: { filename }')
        return


if __name__ == '__main__':
    print('FTP Cliente Prueba Iniciada'.center(100, '-'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        TCPClientSocket.connect(('192.168.0.8', 8888))
        ftp_client: FTPClient = FTPClient(TCPClientSocket, 'Servidor FTP/TCP')
        msg_rcv: str = ftp_client.recibir_mensajes()
        msg_env: str = ''
        print(msg_rcv)
        if ftp_client.validacion():
            print(f'Acceso aceptado por [{ ftp_client.nombre }]...')
            msg_rcv = ftp_client.recibir_mensajes()
            print('\n', msg_rcv)
            msg_env = in_data('Archivo a descargar: ')
            ftp_client.enviar_menssaje(msg_env)
            ftp_client.transferencia_archivo(msg_env, 8181)
        else:
            print(f'Acceso denegado por [{ ftp_client.nombre }]...')
    print('FTP Cliente Prueba Finalizada'.center(100, '-'))
