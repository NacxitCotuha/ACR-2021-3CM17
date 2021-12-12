from concurrent import futures
import grpc
import json
import logging
import os
import shutil
from Practicas.Practica05.Proto import practica05_pb2_grpc
from Practicas.Practica05.Proto import practica05_pb2
# import Practicas.Practica05.Proto.practica05_pb2_grpc as practica05_pb2_grpc


def validacion_json(usuario: str, password: str) -> tuple[str, str, bool]:
    print(f'Inicio sesion de {usuario} con password {password}')
    with open('users.json') as file:
        file_json = json.load(file)
        cliente_mensaje: str
        cliente_directorio: str
        acceso: bool
        for cliente in file_json['usuarios']:
            if (usuario == cliente['username']) and (password == cliente['password']):
                cliente_mensaje = f'Acceso Aceptado para {usuario}'
                cliente_directorio = cliente['directorio']
                acceso = True
                break
        else:
            cliente_mensaje = f'Acceso Denegado para {usuario}'
            cliente_directorio = 'No Existe'
            acceso = False
    datos_cliente: tuple[str, str, bool] = (cliente_directorio, cliente_mensaje, acceso)
    return datos_cliente


def crear_archivo(directorio_principal: str, directorio: str, nombre_archivo: str) -> tuple[str, bool]:
    creacion: tuple[str, bool]
    path_completo: str = directorio_principal + directorio + nombre_archivo
    if os.path.isfile(path_completo):
        creacion = (f'El archivo [{nombre_archivo}] ya existe', False)
        return creacion
    else:
        dividir_nombre = nombre_archivo.split(sep='.', maxsplit=5)
        if (dividir_nombre[len(dividir_nombre)-1] == 'txt') and (len(dividir_nombre) >= 2):
            try:
                file = open(path_completo, 'x')
                file.close()
                creacion = (f'Archivo [{nombre_archivo}] se ha creado Correctamente', True)
                return creacion
            except FileNotFoundError as e:
                creacion = (f'Ha ocurrido un error al crear el archivo [{nombre_archivo}] \n {e}', False)
                return creacion
        else:
            creacion = (f'Ha ocurrido un error al crear el archivo [{nombre_archivo}] en {path_completo}', False)
            return creacion


def leer_archivo(directorio_principal: str, directorio: str, nombre_archivo: str) -> str:
    path_completo: str = directorio_principal + directorio + nombre_archivo
    try:
        with open(path_completo, 'r') as file:
            for linea in file:
                yield linea
    except FileNotFoundError as e:
        mensajes: list[str] = [f'El Archivo [{nombre_archivo}] no se encntro en {directorio}',
                               f'Directorio archivo: {path_completo}']
        print(e)
        for mensaje in mensajes:
            yield mensaje


def escribir_archivo(directorio_principal: str, directorio: str, nombre_archivo: str, texto: str) -> tuple[str, bool]:
    path_completo: str = directorio_principal + directorio + '/' + nombre_archivo
    escritura_operacion: tuple[str, bool]
    try:
        with open(path_completo, 'a') as file:
            file.write(texto)
        escritura_operacion = (f'Escritura completada en archivo [{nombre_archivo}]', True)
        return escritura_operacion
    except FileNotFoundError as e:
        escritura_operacion = (f'Escritura No se pudo hacer en Archivo [{nombre_archivo}] error: \n{e}', False)
        return escritura_operacion


def eliminar_archivo(directorio_principal: str, directorio: str, nombre_archivo: str) -> tuple[str, bool]:
    operacion: tuple[str, bool]
    path_completo: str = directorio_principal + directorio + nombre_archivo
    if os.path.isfile(path_completo):
        os.remove(path_completo)
        operacion = (f'Archivo [{nombre_archivo}] ha sido eliminado de la ruta [{path_completo}]', True)
        return operacion
    else:
        operacion = (f'Archivo [{nombre_archivo}] no existe en la ruta', False)
        return operacion


def renombrar_archivo(directorio_principal: str, directorio: str, objetivo: str, nombre: str) -> tuple[str, bool]:
    operacion: tuple[str, bool]
    path_completo: str = directorio_principal + directorio + objetivo
    nuevo_nombre: str = directorio_principal + directorio + nombre
    if os.path.isfile(path_completo):
        dividir_nombre = nombre.split(sep='.', maxsplit=5)
        if (dividir_nombre[len(dividir_nombre) - 1] == 'txt') and (len(dividir_nombre) >= 2):
            os.rename(path_completo, nuevo_nombre)
            operacion = (f'El archivo [{objetivo}] ha cambiado de nombre a [{nombre}] de manera exitosa', True)
            return operacion
        else:
            operacion = (f'El nombre [{nombre}] no es un nombre valido', False)
            return operacion
    else:
        operacion = (f'El Archivo [{objetivo}] no existe en [{directorio_principal + directorio}]', False)
        return operacion


def crear_directorio(directorio_principal: str, directorio_actual: str, directorio_modificar: str) -> tuple[str, bool]:
    crear_operacion: tuple[str, bool]
    path_completo: str = directorio_principal + directorio_actual + '/' + directorio_modificar
    if not os.path.isdir(path_completo):
        if not os.path.isdir(path_completo):
            try:
                os.mkdir(path_completo)
                crear_operacion = (
                    f'La creacion del nuevo directorio [{directorio_modificar}] ha sido completada correctamente', True
                )
                return crear_operacion
            except FileExistsError as e:
                crear_operacion = (f'Ha ocurrido un error: \n{e}', False)
                return crear_operacion
        else:
            crear_operacion = ('La direccion proporcionada es un archivo no un directorio', False)
            return crear_operacion
    else:
        crear_operacion = ('La direccion proporcionada ya existe en su ubicacion actual', False)
        return crear_operacion


def eliminar_directorio(directorio_principal: str,
                        directorio_actual: str,
                        directorio_modificar: str) -> tuple[str, bool]:
    eliminar_operacion: tuple[str, bool]
    path_completo: str = directorio_principal + directorio_actual + directorio_modificar
    if os.path.isdir(path_completo):
        shutil.rmtree(path_completo)
        eliminar_operacion = (f'El directorio [{directorio_modificar}] fue borrado', True)
        return eliminar_operacion
    else:
        eliminar_operacion = ('El directorio no existe o no se encuentra', False)
        return eliminar_operacion


def lista_directorios(directorio: str) -> str:
    elementos = os.listdir(directorio)
    for elemento in elementos:
        yield elemento
    return


def cambiar_directorio(directorio_principal: str,
                       directorio_actual: str,
                       directorio_modificar: str) -> tuple[str, bool]:
    cambiar: tuple[str, bool]
    path_completo = directorio_principal + directorio_actual + '/' + directorio_modificar
    if os.path.isdir(path_completo):
        cambiar = (directorio_actual + '/' + directorio_modificar, True)
        return cambiar
    else:
        cambiar = (f'No se encontro el directorio [{directorio_modificar}]', False)
        return cambiar


class TransferenciaDatos(practica05_pb2_grpc.OperacionesDFSServicer):
    def ValidacionUsuario(self, request, context):
        datos_cliente = validacion_json(usuario=request.nombre, password=request.password)
        return practica05_pb2.RespuestaUsuario(directorio_principal=datos_cliente[0],
                                               mensaje_validacion=datos_cliente[1],
                                               acceso=datos_cliente[2])

    def CrearArchivo(self, request, context):
        operacion = crear_archivo(directorio_principal=request.directorio_principal,
                                  directorio=request.directorio_archivo,
                                  nombre_archivo=request.nombre_archivo)
        return practica05_pb2.RespuestaArchivo(
            mensaje_completado=operacion[0],
            operacion_completada=operacion[1])

    def LeerArchivo(self, request, context):
        lectura = leer_archivo(directorio_principal=request.directorio_principal,
                               directorio=request.directorio_archivo,
                               nombre_archivo=request.nombre_archivo)
        for linea_texto in lectura:
            yield practica05_pb2.RespuestaLectura(datos_archivo=linea_texto)

    def EscrituraArchivo(self, request, context):
        escritura = escribir_archivo(directorio_principal=request.directorio_principal,
                                     directorio=request.directorio_archivo,
                                     nombre_archivo=request.nombre_archivo,
                                     texto=request.texto_escribir)
        return practica05_pb2.RespuestaArchivo(mensaje_completado=escritura[0],
                                               operacion_completada=escritura[1])

    def EscrituraMultipleArchivo(self, request_iterator, context):
        escritura: tuple[str, bool] = ('Ejecutando operacion Escritura', True)
        for request in request_iterator:
            escritura = escribir_archivo(directorio_principal=request.directorio_principal,
                                         directorio=request.directorio_archivo,
                                         nombre_archivo=request.nombre_archivo,
                                         texto=request.texto_escribir)
            if not escritura[1]:
                return practica05_pb2.RespuestaArchivo(mensaje_completado=escritura[0],
                                                       operacion_completada=escritura[1])
        return practica05_pb2.RespuestaArchivo(mensaje_completado=escritura[0],
                                               operacion_completada=escritura[1])

    def EliminarArchivo(self, request, context):
        eliminacion_operacion = eliminar_archivo(directorio_principal=request.directorio_principal,
                                                 directorio=request.directorio_archivo,
                                                 nombre_archivo=request.nombre_archivo)
        return practica05_pb2.RespuestaArchivo(mensaje_completado=eliminacion_operacion[0],
                                               operacion_completada=eliminacion_operacion[1])

    def RenombrarArchivo(self, request, context):
        renombrar_operacion = renombrar_archivo(directorio_principal=request.directorio_principal,
                                                directorio=request.directorio_actual,
                                                objetivo=request.archivo_objetivo,
                                                nombre=request.nombre_cambiar)
        return practica05_pb2.RespuestaArchivo(mensaje_completado=renombrar_operacion[0],
                                               operacion_completada=renombrar_operacion[1])

    def CrearDirectorio(self, request, context):
        creacion = crear_directorio(directorio_principal=request.directorio_principal,
                                    directorio_actual=request.directorio_actual,
                                    directorio_modificar=request.directorio_modificar)
        return practica05_pb2.RespuestaModificarDirectorio(mensaje_completado=creacion[0],
                                                           operacion_completada=creacion[1])

    def EliminarDirectorio(self, request, context):
        eliminar = eliminar_directorio(directorio_principal=request.directorio_principal,
                                       directorio_actual=request.directorio_actual,
                                       directorio_modificar=request.directorio_modificar)
        return practica05_pb2.RespuestaModificarDirectorio(mensaje_completado=eliminar[0],
                                                           operacion_completada=eliminar[1])

    def ListaDirectorios(self, request, context):
        listar = lista_directorios(directorio=request.directorio_actual)
        for elemento in listar:
            yield practica05_pb2.RespuestaDirectorios(informacion_directorio=elemento)

    def CambiarDirectorio(self, request, context):
        cambiar = cambiar_directorio(directorio_principal=request.directorio_principal,
                                     directorio_actual=request.directorio_actual,
                                     directorio_modificar=request.directorio_modificar)
        return practica05_pb2.RespuestaModificarDirectorio(mensaje_completado=cambiar[0],
                                                           operacion_completada=cambiar[1])


def main():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    practica05_pb2_grpc.add_OperacionesDFSServicer_to_server(TransferenciaDatos(), servidor)
    servidor.add_insecure_port('[::]:50505')
    servidor.start()
    servidor.wait_for_termination()


if __name__ == '__main__':
    print(f'Servidor DFS'.center(100, '-'))
    logging.basicConfig()
    main()
