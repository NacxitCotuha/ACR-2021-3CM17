import grpc
import socket

# Conexion a Servidor - Balanceador
from Problemas.Problema2_Balanceador.Proto import balanceador_pb2
from Problemas.Problema2_Balanceador.Proto import balanceador_pb2_grpc

# Conexion a Servidor - Servidor N
from Problemas.Problema2_Balanceador.Proto import servidor_n_pb2
from Problemas.Problema2_Balanceador.Proto import servidor_n_pb2_grpc


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


class ServidorNConexion:
    def __init__(self, stub: servidor_n_pb2_grpc.TransferDataStub, localhost: str, servidor: str) -> None:
        self._stub: servidor_n_pb2_grpc.TransferDataStub = stub
        self._request: servidor_n_pb2 = servidor_n_pb2
        self._localhost: str = localhost
        self._servidor: str = servidor
        return

    def _generar_iterador(self, lista: list[str]):
        for item in lista:
            saludo = self._request.ReqSaludo(nombre=item)
            yield saludo

    def conexion_exitosa(self) -> bool:
        respuesta = self._stub.ConexionExitosa(self._request.ReqConexion(ip=self._localhost))
        print(respuesta.mensaje)
        return respuesta.conexion

    def mensaje_saludo(self) -> None:
        nombre: str = input('Ingrese su nombre: ')
        response = self._stub.MensajeSaludo(self._request.ReqSaludo(nombre=nombre))
        print(f'Respuesta del servidor [{self._servidor}]: {response.saludo}')
        return

    def mensaje_saludo_varios_idiomas(self) -> None:
        nombre: str = input('Ingrese su nombre: ')
        for response in self._stub.MensajeSaludoVariosIdiomas(self._request.ReqSaludo(nombre=nombre)):
            print(f'Respuesta Stream del Servidor [{self._servidor}]: {response.saludo}')

    def mensaje_saludo_amigos(self) -> None:
        solicitud: bool = True
        amigos: list[str] = []
        while solicitud:
            try:
                no_amigos: int = int(input('Numero de Amigos a Saludar: '))
                for no_amigo in range(no_amigos):
                    amigo: str = input(f'Ingrese el nombre de amigo [{no_amigo}]:')
                    amigos.append(amigo)
                solicitud = False
                continue
            except ValueError:
                solicitud = True
                continue
        response = self._stub.MensajeSaludoAmigos(self._generar_iterador(lista=amigos))
        print(f'Respuesta del servidor [{self._servidor}] a Saluda a mis amigos:')
        print(f'Peticion stream, total de mensajes recibidos: {response.contador_nombres}'.rjust(5, ' '))
        print(f'Mensaje concatenado: {response.saludo}'.rjust(5, ' '))
        return

    def mensaje_saludo_amigos_varios_idiomas(self) -> None:
        solicitud: bool = True
        amigos: list[str] = []
        while solicitud:
            try:
                no_amigos: int = int(input('Numero de Amigos a Saludar: '))
                for no_amigo in range(no_amigos):
                    amigo: str = input(f'Ingrese el nombre de amigo [{no_amigo}]:')
                    amigos.append(amigo)
                solicitud = False
                continue
            except ValueError:
                solicitud = True
                continue
        for response in self._stub.MensajeSaludoAmigosVariosIdiomas(self._generar_iterador(lista=amigos)):
            print(f'Servidor [{self._servidor}] dice: {response.saludo}')
        return

    def remove_conexion(self) -> None:
        response = self._stub.RemoveConexion(self._request.ReqConexion(ip=self._localhost))
        print(response.mensaje)
        return


def conexion_servidor_balanceador() -> str:
    localhost: str = get_localhost()
    with grpc.insecure_channel('192.168.0.2:5050') as channel:
        stub: balanceador_pb2_grpc.TransferDataStub = balanceador_pb2_grpc.TransferDataStub(channel)
        response = stub.ServidorN(balanceador_pb2.ReqServidor(ip=localhost))
        while not ('.' in response.host_servidor):
            response = stub.ServidorN(balanceador_pb2.ReqServidor(ip=localhost))
    return response.host_servidor


def conexion_servidor_n(servidor: str) -> None:
    localhost: str = get_localhost()
    with grpc.insecure_channel(servidor) as channel:
        stub: servidor_n_pb2_grpc.TransferDataStub = servidor_n_pb2_grpc.TransferDataStub(channel)
        servidor_n: ServidorNConexion = ServidorNConexion(stub=stub, localhost=localhost, servidor=servidor)
        if servidor_n.conexion_exitosa():
            servidor_n.mensaje_saludo()
            servidor_n.mensaje_saludo_varios_idiomas()
            servidor_n.mensaje_saludo_amigos()
            servidor_n.mensaje_saludo_amigos_varios_idiomas()
            servidor_n.remove_conexion()
    return


def main() -> None:
    servidor = conexion_servidor_balanceador()
    conexion_servidor_n(servidor=servidor)
    return


if __name__ == '__main__':
    print('Cliente Balanceador'.center(100, '-'))
    main()
