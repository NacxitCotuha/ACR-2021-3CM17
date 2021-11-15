import json
import socket


class RootDNS:
    def __init__(self, consulta: str, conn: socket.socket, addr) -> None:
        # Consexion:
        self._conn: socket.socket = conn
        self._addr = addr
        self._consulta: str = consulta

        # Datos a conseguir
        self._ttl: int = 0
        self._clase: str = ''
        self._type: str = ''
        self._ip: str = ''
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
        with open('root-server-TLDs.json') as file:
            file_json = json.load(file)
            if file_json[self._consulta]:
                datos = file_json[self._consulta]
                self._ttl = datos['TTL']
                self._clase = datos['Class']
                self._type = datos['Type']
                self._ip = datos['Address']
                self._port = datos['Port']
                busqueda = True
            else:
                busqueda = False
        return busqueda

    def get_info(self) -> str:
        info: str = f'{ self._ttl }, { self._clase }, { self._type }, { self._ip }, { self._port }'
        return info


if __name__ == '__main__':
    print('Servidor DNS Raíz'.center(100, '-'))
    localhost: str = socket.gethostbyname(socket.gethostname())
    localport: int = 5555
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerRootDNS:
        UDPServerRootDNS.bind((localhost, localport))
        print(f'Servidor UDP [DNS Raíz:{localhost}:{localport}] activo, esperando peticiones...')
        consulta_str: str
        while True:
            consulta_bytes, address = UDPServerRootDNS.recvfrom(1024)
            consulta_str = consulta_bytes.decode('utf-8')
            rootDNS: RootDNS = RootDNS(consulta_str, UDPServerRootDNS, address)
            if rootDNS.verificar_consulta():
                if rootDNS.consulta_json():
                    msg_env: str = rootDNS.get_info()
                    rootDNS.enviar_mensaje(msg_env)
                else:
                    rootDNS.enviar_mensaje(f'Error: 404 No se encuentra la info en Server Root DNS')
            else:
                rootDNS.enviar_mensaje(f'Error: Consulta Invalida "{ consulta_bytes }"')
    # Final Codigo
