import socket
import os
import sys
import time

from ConnSocket import ConnSocket


def in_data() -> str:
    __data: str = ''
    while __data == '':
        __data = input('R = ')
        sys.stdout.flush()
    return __data


def error(_mensaje: str):
    print(f'Error: {_mensaje} no es, introducir nuevamente el dato')


def introducir_eje(_eje: str) -> str:
    __msg_input: str = ''
    __errorEje: bool = True
    while __errorEje:
        __msg_input = in_data()
        try:
            coordenada = int(__msg_input)
            print(f'Coordenada {coordenada} del {_eje} si es un numero entero')
            __errorEje = False
        except Exception as e:
            print(e)
            print(f'Introduce correctamente el {_eje}: ')
            __errorEje = True
        finally:
            continue

    return __msg_input


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <HOST> <PORT>')
        sys.exit(1)
    HOST: str = str(sys.argv[1])
    PORT: int = int(sys.argv[2])
    flag: int
    msg_rcv: str
    msg_env: str
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        TCPClientSocket.connect((HOST, PORT))
        print("Conectando...")
        conn = ConnSocket(TCPClientSocket, 'Servidor')
        jugador = conn.recibir()
        conexion = True
        while conexion:
            flag = conn.recibir_flag()
            clear_console()

            if flag == 0:
                print(f'======{jugador}=====')
                msg_rcv = conn.recibir()
                # print(msg_rcv)
                conexion = False
                print(f'FIN DEL JUEGO....')
                time.sleep(5)
                continue
            elif flag == 1:
                print(f'======{jugador}=====')
                msg_rcv = conn.recibir()
                # print(msg_rcv)
                continue
            elif flag == 2:
                print(f'======{jugador}=====')
                flagGame: int
                msg_rcv = conn.recibir()
                if msg_rcv == '':
                    print(f' Ocurrio un error fatal')
                    conexion = False
                    continue
                else:
                    # Se introducen los ejes y se envian para comprobar
                    msg_env = introducir_eje('Eje X')
                    conn.enviar(msg_env)
                    msg_rcv = conn.recibir()
                    if msg_rcv == '':
                        print(f' Ocurrio un error fatal')
                        conexion = False
                        continue
                    else:
                        msg_env = introducir_eje('Eje Y')
                        conn.enviar(msg_env)
                        errorCoor = conn.recibir()

                        while errorCoor == 'error':
                            msg_env = introducir_eje('Eje X')
                            conn.enviar(msg_env)
                            msg_rcv = conn.recibir()
                            msg_env = introducir_eje('Eje Y')
                            conn.enviar(msg_env)
                            errorCoor = conn.recibir()
                        else:
                            if errorCoor == 'accept':
                                continue
                            else:
                                print('Posiblemente ocurio un grave error revise por favor')
                                conexion = False
                                continue

            elif flag == 3:
                print(f'======{jugador}=====')
                print(f'A la espera de otros jugadores')
                continue
            else:
                print(f'======{jugador}=====')
                print(f'Algo salio mal recibiste como flag: {flag}')
                conexion = False
