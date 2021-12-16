from concurrent import futures
import grpc
import logging
import socket
import sys

# Trabajo Servidor
from Problemas.Problema2_Balanceador.Proto import servidor_n_pb2
from Problemas.Problema2_Balanceador.Proto import servidor_n_pb2_grpc

CONECTADOS: int = 0
PUERTO: int
LOCALHOST: str
LISTA_SALUDOS: list[str] = ['Hello', 'Salut', 'Hallo', 'Hola', 'Merhaba']


def get_localhost() -> str:
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localhost: str
    try:
        st.connect(('10.255.255.255', 1))
        localhost = st.getsockname()[0]
    except ConnectionError:
        localhost = '127.0.0.1'
    finally:
        st.close()
    return localhost


def servidor_conexiones(tipo: str) -> tuple[str, int]:
    global PUERTO, CONECTADOS, LOCALHOST
    respuesta: tuple[str, int]
    if tipo == 'servidor':
        print('Peticion del servidor balanceador correcta')
    else:
        print('Peticion del servidor balanceador incorrecta')
    respuesta = (LOCALHOST, CONECTADOS)
    return respuesta


def conexion_exitosa(ip: str) -> tuple[bool, str]:
    respuesta: tuple[bool, str]
    global CONECTADOS, LOCALHOST
    print(f'El cliente [{ip}] ha solicitado unirse...')
    if CONECTADOS < 100:
        CONECTADOS += 1
        print(f'El cliente [{ip}] se ha unido de manera correcta')
        print(f'Gente conectada: {CONECTADOS}')
        respuesta = (True, f'Conexion exitosa con el Servidor [{LOCALHOST}]')
    else:
        respuesta = (False, f'Lo sentimos pero no se puede conectar con el servidor [{LOCALHOST}]')
    return respuesta


def remove_conexion(ip: str) -> tuple[bool, str]:
    respuesta: tuple[bool, str]
    global CONECTADOS, LOCALHOST
    CONECTADOS -= 1
    if CONECTADOS >= 0:
        print(f'El cliente [{ip}] se ha desconectador de manera correcta')
        print(f'Gente conectada: {CONECTADOS}')
    else:
        print('Ha ocurrido un error')
        print(f'Gente conectada: {CONECTADOS}')
        CONECTADOS = 0
    respuesta = (True, f'Se ha desconectado correctamente del servidor [{LOCALHOST}]')
    return respuesta


class ServidorN(servidor_n_pb2_grpc.TransferDataServicer):
    def ServidorConexiones(self, request, context):
        response = servidor_conexiones(tipo=request.tipo)
        return servidor_n_pb2.ResServidor(
            host=response[0],
            conexiones=response[1]
        )

    def ConexionExitosa(self, request, context):
        response = conexion_exitosa(ip=request.ip)
        return servidor_n_pb2.ResConexion(
            conexion=response[0],
            mensaje=response[1]
        )

    # Operaciones de SALUDOS
    def MensajeSaludo(self, request, context):
        return servidor_n_pb2.ResSaludo(saludo=f'Hola {request.nombre}')

    def MensajeSaludoVariosIdiomas(self, request, context):
        global LISTA_SALUDOS
        for idioma in LISTA_SALUDOS:
            yield servidor_n_pb2.ResSaludo(saludo=f'{idioma}, {request.nombre}')

    def MensajeSaludoAmigos(self, request_iterator, context):
        contador: int = 0
        saludos: str = 'Hola'
        for request in request_iterator:
            contador += 1
            saludos += f', {request.nombre}'
        return servidor_n_pb2.ResResumenSaludo(
            contador_nombres=contador,
            saludo=saludos
        )

    def MensajeSaludoAmigosVariosIdiomas(self, request_iterator, context):
        global LISTA_SALUDOS
        for request in request_iterator:
            for idioma in LISTA_SALUDOS:
                yield servidor_n_pb2.ResSaludo(saludo=f'{idioma}, {request.nombre}')

    def RemoveConexion(self, request, context):
        response = remove_conexion(ip=request.ip)
        return servidor_n_pb2.ResConexion(
            conexion=response[0],
            mensaje=response[1]
        )


def main() -> None:
    global PUERTO, LOCALHOST
    if len(sys.argv) != 2:
        print(f'Usar: {sys.argv[0]} <PUERTO: int>')
        sys.exit(1)
    try:
        PUERTO = int(sys.argv[1])
    except ValueError:
        print(f'Usar: {sys.argv[0]} <PUERTO: int>')
        sys.exit(1)
    host: str = f'[::]:{PUERTO}'
    LOCALHOST = f'{get_localhost()}:{PUERTO}'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=102))
    servidor_n_pb2_grpc.add_TransferDataServicer_to_server(ServidorN(), server)
    server.add_insecure_port(host)
    server.start()
    server.wait_for_termination()
    return


if __name__ == '__main__':
    logging.basicConfig()
    main()
