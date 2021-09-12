import socket
import os
import sys


def in_data() -> str:
    __data: str = ''
    while __data == '':
        __data = input(f'R = ')
        sys.stdout.flush()
    return __data


def error(mensaje: str):
    print(f'Error: {mensaje} no es, introducir nuevamente el dato')


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


HOST = '192.168.0.2'
PORT = 65432
buffer_size = 1024
conexion: bool = True
mensaje_env: str
mensaje_recv: str

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Conectando...")

    def recibir() -> str:
        __data = b''
        while __data == b'':
            __data = TCPClientSocket.recv(buffer_size)
        return __data.decode('utf-8')

    def enviar(mensaje: str):
        __data = str.encode(mensaje)
        TCPClientSocket.sendall(__data)
        return


    enviar(f'Hola Servidor TCP')
    print('Esperando una respuesta...')
    mensaje_recv = recibir()
    print(f'Recibido: {mensaje_recv} de {TCPClientSocket.getpeername()}, conexion establecida')

    while conexion:
        mensaje_recv = recibir()
        print(mensaje_recv)
        mensaje_env = in_data()
        enviar(mensaje_env)

        mensaje_recv = recibir()

        if mensaje_recv == 'Salir':
            conexion = False
            print(f'Conexion terminada con: {TCPClientSocket.getpeername()}')
            continue
        elif mensaje_recv == 'Error':
            clear_console()
            error(mensaje_env)
            continue

        estado_juego = True
        while estado_juego:
            # Eje x
            # mensaje_recv = recibir()
            print(mensaje_recv)
            mensaje_env = in_data()
            enviar(mensaje_env)

            # Eje y
            clear_console()
            mensaje_recv = recibir()
            print(mensaje_recv)
            mensaje_env = in_data()
            enviar(mensaje_env)

            mensaje_recv = recibir()
            if mensaje_recv == 'Error':
                clear_console()
                mensaje_recv = recibir()
                error(mensaje_recv)

                # Eje X Se recibe y se reinicia el while
                mensaje_recv = recibir()
                continue

            elif mensaje_recv == 'Perdiste':
                clear_console()
                # Recibe los datos de la partida
                mensaje_recv = recibir()
                print(mensaje_recv)
                estado_juego = False
                continue

            elif mensaje_recv == 'Ganaste':
                clear_console()
                # Recibe los datos de la partida
                mensaje_recv = recibir()
                print(mensaje_recv)
                estado_juego = False
                continue

            clear_console()

