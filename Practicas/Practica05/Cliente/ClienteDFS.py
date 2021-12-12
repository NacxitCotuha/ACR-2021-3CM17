import grpc
import logging
import os
from Practicas.Practica05.Proto import practica05_pb2
from Practicas.Practica05.Proto import practica05_pb2_grpc

datos_cliente: dict = {
    'usuario': '',
    'password': '',
    'directorio_usuario': '',
    'directorio_configurable': ''
}


def clear_console() -> None:
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    return


class ClienteOperaciones:
    def __init__(self, stub: practica05_pb2_grpc.OperacionesDFSStub, datos: dict):
        self._stub: practica05_pb2_grpc.OperacionesDFSStub = stub
        self._solicitud: practica05_pb2 = practica05_pb2
        self._datos: dict = datos

    @property
    def directorio(self):
        return self._datos['usuario'] + '/' + self._datos['directorio_configurable']

    def _enviar_mucho_texto(self, texto: list[str], archivo):
        for linea in texto:
            escribir = self._solicitud.SolicitudEscrituraArchivo(
                directorio_principal=self._datos['directorio_usuario'],
                directorio_archivo=self._datos['directorio_configurable'],
                nombre_archivo=archivo,
                texto_escribir=linea
            )
            yield escribir

    # Comando CREATE: Crea el Archivo de Texto
    def comando_create(self, archivo: str) -> None:
        response = self._stub.CrearArchivo(self._solicitud.SolicitudArchivo(
            directorio_principal=self._datos['directorio_usuario'],
            directorio_archivo=self._datos['directorio_configurable'],
            nombre_archivo=archivo))
        if response.operacion_completada:
            print(response.mensaje_completado)
        else:
            print(f'Hubo un Error: {response.mensaje_completado}')
        return

    # Comando READ: Lee el archivo de texto
    def comando_read(self, archivo: str) -> None:
        for response in self._stub.LeerArchivo(
                self._solicitud.SolicitudArchivo(
                    directorio_principal=self._datos['directorio_usuario'],
                    directorio_archivo=self._datos['directorio_configurable'],
                    nombre_archivo=archivo)):
            print(response.datos_archivo, end='')
        print('')
        return

    # Comando WRITE: Escribe en el archivo de Texto
    def comando_write(self, archivo: str) -> None:
        texto: str
        opcion: str = 'y'
        lineas_texto: list[str] = []
        while (opcion == 'Y') or (opcion == 'y'):
            texto = input('Inserte el texto a escribir: ')
            lineas_texto.append(texto + '\n')
            opcion = input('Desea escribir mas Texto(Y:si/N:no): ')
        print(f'Se escribiran {len(lineas_texto)} lineas de texto en el Archivo: {archivo}')
        if len(lineas_texto) == 1:
            self._stub.EscrituraArchivo(self._solicitud.SolicitudEscrituraArchivo(
                directorio_principal=self._datos['directorio_usuario'],
                directorio_archivo=self._datos['directorio_configurable'],
                nombre_archivo=archivo,
                texto_escribir=lineas_texto[0]
            ))
        else:
            self._stub.EscrituraMultipleArchivo(self._enviar_mucho_texto(
                texto=lineas_texto,
                archivo=archivo
            ))
        return

    # Comando REMOVE: Elimina el Archivo de Texto
    def comando_remove(self, archivo: str) -> None:
        response = self._stub.EliminarArchivo(self._solicitud.SolicitudArchivo(
            directorio_principal=self._datos['directorio_usuario'],
            directorio_archivo=self._datos['directorio_configurable'],
            nombre_archivo=archivo))
        if response.operacion_completada:
            print(response.mensaje_completado)
        else:
            print(f'Hubo un Error: {response.mensaje_completado}')
        return

    def comando_rename(self, archivo: str, cambiar: str) -> None:
        response = self._stub.RenombrarArchivo(self._solicitud.SolicitudModificarFichero(
            directorio_principal=self._datos['directorio_usuario'],
            directorio_actual=self._datos['directorio_configurable'],
            archivo_objetivo=archivo,
            nombre_cambiar=cambiar))
        if response.operacion_completada:
            print(response.mensaje_completado)
        else:
            print(f'Hubo un Error: {response.mensaje_completado}')
        return

    # Comando MKDIR: Crear Nuevo SubDirectorio
    def comando_mkdir(self, directorio: str):
        response = self._stub.CrearDirectorio(self._solicitud.SolicitudModificarDirectorio(
            directorio_principal=self._datos['directorio_usuario'],
            directorio_actual=self._datos['directorio_configurable'],
            directorio_modificar=directorio))
        if response.operacion_completada:
            print(response.mensaje_completado)
        else:
            print(f'Hubo un Error: {response.mensaje_completado}')
        return

    # Comando RMDIR: Elimina un directorio y su contenido
    def comando_rmdir(self, directorio: str) -> None:
        response = self._stub.EliminarDirectorio(self._solicitud.SolicitudModificarDirectorio(
            directorio_principal=self._datos['directorio_usuario'],
            directorio_actual=self._datos['directorio_configurable'],
            directorio_modificar=directorio))
        if response.operacion_completada:
            print(response.mensaje_completado)
        else:
            print(f'Hubo un Error: {response.mensaje_completado}')
        return

    # CD: Cambia de directorio
    def comando_cd(self, directorio: str) -> None:
        response = self._stub.CambiarDirectorio(self._solicitud.SolicitudModificarDirectorio(
            directorio_principal=self._datos['directorio_usuario'],
            directorio_actual=self._datos['directorio_configurable'],
            directorio_modificar=directorio))
        if response.operacion_completada:
            self._datos['directorio_configurable'] = response.mensaje_completado
        else:
            print(f'Hubo un Error: {response.mensaje_completado}')
        return

    # Comando READDIR: Ver la lista de directorios
    def comando_readdir(self) -> None:
        directorio: str = self._datos['directorio_usuario']
        if self._datos['directorio_configurable'] != '':
            directorio += '/' + self._datos['directorio_configurable']
        for response in self._stub.ListaDirectorios(
                self._solicitud.SolicitudDirectorio(
                    directorio_actual=directorio)):
            print(response.informacion_directorio)

    # Comando MAN: Ve manual de uso de comandos
    def comando_man(self) -> None:
        for response in self._stub.LeerArchivo(
                self._solicitud.SolicitudArchivo(
                    directorio_principal='',
                    directorio_archivo='./',
                    nombre_archivo='Manual.txt')):
            print(response.datos_archivo, end='')
        print('')
        return


def inicio_sesion(stub: practica05_pb2_grpc.OperacionesDFSStub) -> bool:
    global datos_cliente
    usuario: str = input('Ingrese el nombre de usuario: ').strip()
    password: str = input('Ingrese la contraseña: ').strip()
    response = stub.ValidacionUsuario(practica05_pb2.SolicitudUsuario(nombre=usuario, password=password))
    if response.acceso:
        print(response.mensaje_validacion)
        datos_cliente['usuario'] = usuario
        datos_cliente['password'] = password
        datos_cliente['directorio_usuario'] = response.directorio_principal
        return True
    else:
        print(response.mensaje_validacion)
        return False


def dividir_texto(texto: str) -> list[str]:
    palabras = texto.split(sep=' ', maxsplit=3)
    return palabras


def consola_dfs(cliente: ClienteOperaciones) -> None:
    comando: str = ''
    while comando != 'EXIT':
        comando = ''
        comando_completo: str = input(cliente.directorio + '> ')
        comando_dividido: list[str] = dividir_texto(comando_completo)
        if len(comando_dividido) == 1:
            comando = comando_dividido[0]
            if comando == 'READDIR':
                cliente.comando_readdir()
                continue
            elif comando == 'CLEAR':
                clear_console()
                continue
            elif comando == 'MAN':
                cliente.comando_man()
                continue
            elif comando == 'EXIT':
                print('Desconectandose del ServidorDFS...')
                continue
            else:
                print('Error de comando, el comando:')
                print(comando_completo + ' NO sepudo ejecutar revise que este bien o el manual con MAN')
                continue
        elif len(comando_dividido) == 2:
            comando = comando_dividido[0]
            if comando == 'CREATE':
                cliente.comando_create(archivo=comando_dividido[1])
                continue
            elif comando == 'READ':
                cliente.comando_read(archivo=comando_dividido[1])
                continue
            elif comando == 'WRITE':
                cliente.comando_write(archivo=comando_dividido[1])
                continue
            elif comando == 'REMOVE':
                cliente.comando_remove(archivo=comando_dividido[1])
                continue
            elif comando == 'MKDIR':
                cliente.comando_mkdir(directorio=comando_dividido[1])
                continue
            elif comando == 'RMDIR':
                cliente.comando_rmdir(directorio=comando_dividido[1])
                continue
            elif comando == 'CD':
                cliente.comando_cd(directorio=comando_dividido[1])
                continue
        elif len(comando_dividido) == 3:
            comando = comando_dividido[0]
            if comando == 'RENAME':
                cliente.comando_rename(archivo=comando_dividido[1], cambiar=comando_dividido[2])
            continue
        else:
            print('Error de comando, el comando:')
            print(comando_completo + ' NO sepudo ejecutar revise que este bien o el manual con MAN')
            continue
    return


def main():
    global datos_cliente
    print(f'Cliente DFS'.center(100, '-'))
    with grpc.insecure_channel('localhost:50505') as channel:
        stub: practica05_pb2_grpc.OperacionesDFSStub = practica05_pb2_grpc.OperacionesDFSStub(channel)
        if inicio_sesion(stub):
            cliente = ClienteOperaciones(stub=stub, datos=datos_cliente)
            consola_dfs(cliente=cliente)
        else:
            return


if __name__ == '__main__':
    logging.basicConfig()
    main()
