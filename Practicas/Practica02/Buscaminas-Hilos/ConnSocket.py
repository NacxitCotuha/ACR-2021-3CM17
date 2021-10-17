class ConnSocket:
    def __init__(self, client_conn, jugador):
        self.__jugador = jugador
        self.__clientConn = client_conn
        self.__bufferSize: int = 1024

    def enviar(self, mensaje: str):
        __aux = str.encode(mensaje)
        self.__clientConn.sendall(__aux)
        print(f'Enviando a {self.__jugador}: {mensaje}')
        return

    def recibir(self) -> str:
        __aux = b''
        while __aux == b'':
            __aux = self.__clientConn.recv(self.__bufferSize)
        print(f'Recibido de {self.__jugador}:\n {__aux.decode("utf-8")}')
        return __aux.decode('utf-8')

    def error(self):
        __aux = str.encode('Error')
        self.__clientConn.sendall(__aux)

    def enviar_flag(self, flag: int):
        __str_flag = str(flag)
        __aux = str.encode(__str_flag)
        self.__clientConn.sendall(__aux)
        print(f'Enviando flag a {self.__jugador}: {__str_flag}')
        return

    def recibir_flag(self) -> int:
        __aux = b''
        while __aux == b'':
            __aux = self.__clientConn.recv(self.__bufferSize)
        print(f'Recibiendo flag: {__aux.decode("utf-8")}')
        return int(__aux.decode('utf-8'))
