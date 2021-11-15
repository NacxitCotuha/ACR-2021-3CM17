import json
import socket


class NameTLD:
    def __init__(self, consulta: str, conn: socket.socket, addr) -> None:
        self._conn: socket.socket = conn
        self._consulta: str = consulta
        self._addr = addr

        # Datos a conseguir
        self._dominio: str = ''
        self._ttl: int = 0
        self._clase: str = ''
        self._type: str = ''
        self._ip_addr: str = ''
        self._port: int = 0
        return

    def enviar_mensaje(self, msg: str):
        aux: bytes = str.encode(msg)
        self._conn.sendto(aux, self._addr)
        print(f'Enviando a { self._addr }: "{ msg }"')
        return

    def verificar_consulta(self) -> bool:
        if self._consulta != '':
            return True
        else:
            return False

    def consulta_json(self) -> bool:
        busqueda: bool
        with open('TLD-Server-Registrars.json') as file:
            file_json = json.load(file)
            if file_json[self._consulta]:
                datos = file_json[self._consulta]
                self._dominio = datos['Dominio']
                self._ttl = datos['TTL']
                self._clase = datos['Class']
                self._type = datos['Type']
                self._ip_addr = datos['Address']
                self._port = datos['Port']
                busqueda = True
            else:
                busqueda = False
        return busqueda

    def get_info(self) -> str:
        info: str = f'{self._dominio}, {self._ttl}, {self._clase}, {self._type}, {self._ip_addr}, {self._port}'
        return info


# def consulta_name_tld()


if __name__ == '__main__':
    print('Servidor Nombre TLD'.center(100, '-'))
    localhost: str = socket.gethostbyname(socket.gethostname())
    localport: int = 6666
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerNameTLD:
        UDPServerNameTLD.bind((localhost, localport))
        print(f'Servidor UDP [Nombre TLD: {localhost}:{localport}] activo, esperando peticiones...')
        consulta_str: str
        while True:
            consulta_bytes, address = UDPServerNameTLD.recvfrom(1024)
            consulta_str = consulta_bytes.decode('utf-8')
            nameTLD: NameTLD = NameTLD(consulta_str, UDPServerNameTLD, address)
            if nameTLD.verificar_consulta():
                if nameTLD.consulta_json():
                    msg_env: str = nameTLD.get_info()
                    nameTLD.enviar_mensaje(msg_env)
                else:
                    nameTLD.enviar_mensaje(f'Error: 404 No se encuentra la info en Server NAME TLD')
            else:
                nameTLD.enviar_mensaje(f'Error: Consulta Invalida NAME_TLD "{ consulta_bytes }"')

    # Final Codigo
