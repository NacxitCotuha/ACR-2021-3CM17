from concurrent import futures
import logging

import grpc
import saludos_pb2
import saludos_pb2_grpc

listaSaludos: list[str] = ['Hello', 'Salut', 'Hallo', 'Hola', 'Merhaba']


class Saludos(saludos_pb2_grpc.SaludosServicer):
    def DecirHola(self, request, context):
        return saludos_pb2.RespuestaSaludo(saludo=f'Hola { request.nombre }!')

    def HolaEnVariosIdiomas(self, request, context):
        for idioma in listaSaludos:
            yield saludos_pb2.RespuestaSaludo(saludo=f'{ idioma }, { request.nombre }')

    def SaludaAMisAmigos(self, request_iterator, context):
        contador: int = 0
        saludos: str = 'Hola'
        for request in request_iterator:
            contador += 1
            saludos += f', { request.nombre }'
        return saludos_pb2.ResumenSaludos(contador_nombres=contador, saludo=saludos)

    def SaludaAMisAmigosEnVariosIdiomas(self, request_iterator, context):
        for request in request_iterator:
            for idioma in listaSaludos:
                yield saludos_pb2.RespuestaSaludo(saludo=f'{ idioma }, { request.nombre }')


def servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludos_pb2_grpc.add_SaludosServicer_to_server(Saludos(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    servidor()
