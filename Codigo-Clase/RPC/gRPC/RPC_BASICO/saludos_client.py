from __future__ import print_function

import logging
import grpc
import saludos_pb2
import saludos_pb2_grpc


def rpc_simple(stub: saludos_pb2_grpc):
    response = stub.DecirHola(saludos_pb2.SolicitudSaludo(nombre='Nacxit'))
    print(f'Respuesta de saludo recibida { response.saludo }')


def generar_saludo_iterator():
    lista_amigos: list[str] = ['Juan Carlos', 'Lupita', 'Gabriela', 'Nayeli', 'Angela']
    for item in lista_amigos:
        saludo = saludos_pb2.SolicitudSaludo(nombre=item)
        yield saludo


def rpc_response_stream(stub: saludos_pb2_grpc):
    # lista_amigos: list[str] = ['Juan Carlos', 'Lupita', 'Gabriela', 'Nayeli', 'Angela']
    for respuesta in stub.HolaEnVariosIdiomas(saludos_pb2.SolicitudSaludo(nombre='Nacxit')):
        print(f'Response stream: { respuesta.saludo }')


def rpc_request_stream(stub):
    response = stub.SaludaAMisAmigos(generar_saludo_iterator())
    print(f'''
        Peticion stream, total de mensajes recibidos: {str(response.contador_nombres)}
        Mensaje concatenado: {response.saludo}''')


def rpc_bidireccional(stub):
    for respuesta in stub.SaludaAMisAmigosEnVariosIdiomas(generar_saludo_iterator()):
        print(f'Respuesta bidireccional: { respuesta.saludo }')


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = saludos_pb2_grpc.SaludosStub(channel)

        # Llamada a RPC simple
        rpc_simple(stub)

        # Llamada a RPC con respuesta tipo transmisión
        rpc_response_stream(stub)

        # Llamada a RPC con solicitud tipo transmisión
        rpc_request_stream(stub)

        # Llamada a RPC con solicitud y respuesta de tipo transmisión (bidireccional)
        rpc_bidireccional(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
