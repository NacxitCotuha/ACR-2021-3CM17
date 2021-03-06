# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import saludos_pb2 as saludos__pb2


class SaludosStub(object):
    """Definición del servicio saludo
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DecirHola = channel.unary_unary(
                '/holaMundoRPC.Saludos/DecirHola',
                request_serializer=saludos__pb2.SolicitudSaludo.SerializeToString,
                response_deserializer=saludos__pb2.RespuestaSaludo.FromString,
                )
        self.HolaEnVariosIdiomas = channel.unary_stream(
                '/holaMundoRPC.Saludos/HolaEnVariosIdiomas',
                request_serializer=saludos__pb2.SolicitudSaludo.SerializeToString,
                response_deserializer=saludos__pb2.RespuestaSaludo.FromString,
                )
        self.SaludaAMisAmigos = channel.stream_unary(
                '/holaMundoRPC.Saludos/SaludaAMisAmigos',
                request_serializer=saludos__pb2.SolicitudSaludo.SerializeToString,
                response_deserializer=saludos__pb2.ResumenSaludos.FromString,
                )
        self.SaludaAMisAmigosEnVariosIdiomas = channel.stream_stream(
                '/holaMundoRPC.Saludos/SaludaAMisAmigosEnVariosIdiomas',
                request_serializer=saludos__pb2.SolicitudSaludo.SerializeToString,
                response_deserializer=saludos__pb2.RespuestaSaludo.FromString,
                )


class SaludosServicer(object):
    """Definición del servicio saludo
    """

    def DecirHola(self, request, context):
        """UN RPC SIMPLE
        Envia un saludo usando un RPC sencillo 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HolaEnVariosIdiomas(self, request, context):
        """Un RPC con solicitud tipo transmisión
        Recibe una solicitud de saludo y envía una secuencia de mensajes en varios idiomas 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaludaAMisAmigos(self, request_iterator, context):
        """Un RPC con solicitud de tipo transmisión
        Acepta un flujo de datos de tipo saludo y regresa un resumen. 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaludaAMisAmigosEnVariosIdiomas(self, request_iterator, context):
        """Un RPC con transmisión bidireccional
        Acepta un flujo de datos de tipo saludo y envía una secuencia de mensajes del saludo en varios idiomas
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SaludosServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DecirHola': grpc.unary_unary_rpc_method_handler(
                    servicer.DecirHola,
                    request_deserializer=saludos__pb2.SolicitudSaludo.FromString,
                    response_serializer=saludos__pb2.RespuestaSaludo.SerializeToString,
            ),
            'HolaEnVariosIdiomas': grpc.unary_stream_rpc_method_handler(
                    servicer.HolaEnVariosIdiomas,
                    request_deserializer=saludos__pb2.SolicitudSaludo.FromString,
                    response_serializer=saludos__pb2.RespuestaSaludo.SerializeToString,
            ),
            'SaludaAMisAmigos': grpc.stream_unary_rpc_method_handler(
                    servicer.SaludaAMisAmigos,
                    request_deserializer=saludos__pb2.SolicitudSaludo.FromString,
                    response_serializer=saludos__pb2.ResumenSaludos.SerializeToString,
            ),
            'SaludaAMisAmigosEnVariosIdiomas': grpc.stream_stream_rpc_method_handler(
                    servicer.SaludaAMisAmigosEnVariosIdiomas,
                    request_deserializer=saludos__pb2.SolicitudSaludo.FromString,
                    response_serializer=saludos__pb2.RespuestaSaludo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'holaMundoRPC.Saludos', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Saludos(object):
    """Definición del servicio saludo
    """

    @staticmethod
    def DecirHola(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/holaMundoRPC.Saludos/DecirHola',
            saludos__pb2.SolicitudSaludo.SerializeToString,
            saludos__pb2.RespuestaSaludo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HolaEnVariosIdiomas(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/holaMundoRPC.Saludos/HolaEnVariosIdiomas',
            saludos__pb2.SolicitudSaludo.SerializeToString,
            saludos__pb2.RespuestaSaludo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaludaAMisAmigos(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/holaMundoRPC.Saludos/SaludaAMisAmigos',
            saludos__pb2.SolicitudSaludo.SerializeToString,
            saludos__pb2.ResumenSaludos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaludaAMisAmigosEnVariosIdiomas(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/holaMundoRPC.Saludos/SaludaAMisAmigosEnVariosIdiomas',
            saludos__pb2.SolicitudSaludo.SerializeToString,
            saludos__pb2.RespuestaSaludo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
