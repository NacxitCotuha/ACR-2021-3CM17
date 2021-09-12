import socket
import time
from Buscaminas import Buscaminas

HOST = "192.168.0.2"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024
mensaje_env: str
mensaje_recv: str
coor_x: int
coor_y: int
juego = None
dificultad: str

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print('El servidor TCP está disponible y en espera de solicitudes')
    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        def error():
            __aux = str.encode('Error')
            Client_conn.sendall(__aux)

        def recibir() -> str:
            __aux = b''
            while __aux == b'':
                __aux = Client_conn.recv(buffer_size)
            print(f'Recibido: \n{__aux.decode("utf-8")}')
            return __aux.decode('utf-8')

        def enviar(mensaje: str):
            __aux = str.encode(mensaje)
            Client_conn.sendall(__aux)
            print(f'Enviado: \n{mensaje}')
            return

        print(f'Conectando a {Client_addr}')
        conn_jugador = True
        print('Esperando a recibir datos...')
        mensaje_recv = recibir()
        print(f'Recibido: {mensaje_recv} de {Client_addr}')

        print(f'Enviando respuesta a {Client_addr}')
        enviar(f'Hola usuario vamos a jugar')
        conexion: bool = True
        mensaje_env = f''

        while conexion:
            mensaje_env = f'''
Buscaminas - MENU
    1 - Nuevo Juego (Nivel Principiante), Tablero = 9 x 9, Minas = 10
    2 - Nuevo Juego (Nivel Avanzado), Tablero = 16 x 16, Minas = 40
    3 - Salir
'''
            enviar(mensaje_env)
            mensaje_recv = recibir()

            if mensaje_recv == '1':
                juego = Buscaminas(1)
                dificultad = 'Principiante'
            elif mensaje_recv == '2':
                juego = Buscaminas(2)
                dificultad = 'Avanzado'
            elif mensaje_recv == '3':
                print(f'Conexion terminada con {Client_addr}')
                enviar('Salir')
                conexion = False
                continue
            else:
                enviar('Error')
                continue

            INICIO = time.time()
            estado_juego = True
            while estado_juego:
                # Obtiene el eje x
                mensaje_env = juego.imprimir_mapa()
                mensaje_env += f'''
Inserte las coordenadas (x, y) = (columna, fila)...
Columna - Eje X (int):
'''
                enviar(mensaje_env)
                mensaje_recv = recibir()
                coor_x = int(mensaje_recv)

                # Obtiene el eje y
                mensaje_env = juego.imprimir_mapa()
                mensaje_env += f'''
Inserte las coordenadas (x, y) = (columna, fila)...
Fila - Eje Y (int):
'''
                enviar(mensaje_env)
                mensaje_recv = recibir()
                coor_y = int(mensaje_recv)

                aux: bool = juego.in_coor(coor_x, coor_y)

                if not aux:
                    enviar('Error')
                    time.sleep(1)
                    enviar(f'Coordenadas ({coor_x},{coor_y})')
                    time.sleep(1)
                    continue

                aux = juego.jugar_new_coor()

                if not aux:
                    enviar('Perdiste')
                    FINAL = time.time()
                    mensaje_env = juego.imprimir_mapa()
                    TOTAL_TIME = FINAL - INICIO
                    mensaje_env += f'''
Haz Perdido
Dificultad: {dificultad}
Puntaje Total = {juego.puntaje}
Tiempo total de la partida = {TOTAL_TIME: .2f} segundos
'''
                    time.sleep(1)
                    enviar(mensaje_env)
                    time.sleep(1)
                    estado_juego = False
                    continue

                aux = juego.state_juego()

                if aux:
                    enviar('Ganaste')
                    FINAL = time.time()
                    mensaje_env = juego.imprimir_mapa()
                    TOTAL_TIME = FINAL - INICIO
                    mensaje_env += f'''
Felicidades has ganado la partida
Dificultad: {dificultad}
Puntaje Total = {juego.puntaje}
Tiempo total de la partida = {TOTAL_TIME: .2f} segundos
'''
                    time.sleep(1)
                    enviar(mensaje_env)
                    estado_juego = False
                    continue

