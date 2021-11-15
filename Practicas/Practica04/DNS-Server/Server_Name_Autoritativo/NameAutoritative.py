import json
import socket


class NameAutoritative:
    def __init__(self, consulta: str, conn: socket.socket, addr) -> None:
        self._conn: socket.socket = conn
        self._consulta: str = consulta
        self._addr = addr

        # Datos a conseguir
        self._dominio: str = ''
        self._clase: str = ''
        self._tipo: str = ''
        self._addr_dom: str = ''
        return

    def enviar_mensaje(self, msg: str) -> None:
        aux: bytes = str.encode(msg)
        self._conn.sendto(aux, self._addr)
        print(f'Enviando a {self._addr}: "{msg}"')
        return

    def verificar_consulta(self) -> bool:
        if self._consulta != '':
            return True
        else:
            return False

    def consulta_json(self) -> bool:
        busqueda: bool
        with open(f'{ self._consulta }.zone.json') as file:
            file_json = json.load(file)
            if file_json['EOF']:
                datos = file_json['EOF']
                self._dominio = datos['Dominio']
                self._clase = datos['Class']
                self._tipo = datos['Type']
                self._addr_dom = datos['Address']
                busqueda = True
            else:
                busqueda = False
        return busqueda

    def get_info(self) -> str:
        info: str = f'{self._dominio}, {self._clase}, {self._tipo}, {self._addr_dom}'
        if self._dominio != self._consulta:
            info = f'Ocurrio un error al final {self._dominio} es distinto de {self._consulta}'
        return info


if __name__ == '__main__':
    print('Servidor Nombre TLD'.center(100, '-'))
    localhost: str = socket.gethostbyname(socket.gethostname())
    localport: int = 7777
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerNameA:
        UDPServerNameA.bind((localhost, localport))
        print(f'Servidor UDP [Nombre Autoritativo: {localhost}:{localport}] activo, esperando peticiones...')
        consulta_str: str
        while True:
            consulta_bytes, address = UDPServerNameA.recvfrom(1024)
            consulta_str = consulta_bytes.decode('utf-8')
            nameA: NameAutoritative = NameAutoritative(consulta_str, UDPServerNameA, address)
            if nameA.verificar_consulta():
                if nameA.consulta_json():
                    msg_env: str = nameA.get_info()
                    nameA.enviar_mensaje(msg_env)
                else:
                    nameA.enviar_mensaje(f'Error: 404 No se encuentra la info en Server NAME AUTORITATIVE')
            else:
                nameA.enviar_mensaje(f'Error: Consulta Invalida NAME_TLD "{ consulta_bytes }"')
    # Final del codigo
