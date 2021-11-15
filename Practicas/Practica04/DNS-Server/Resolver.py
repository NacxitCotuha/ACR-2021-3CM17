import socket
import threading

LIST_ADDR: list[tuple[str, int]] = []
LIST_THREAD: list[threading.Thread] = []


class Resolver:
    def __init__(self, url: str, conn: socket.socket, addr) -> None:
        self._url: str = url
        self._conn: socket.socket = conn
        self._addr = addr
        self._url_div: list[str] = []

        # Datos Recibidos de Server DNS Root
        self._data_root: list[str] = []  # 0:TTL, 1:Class, 2:Type 3:address_ip 4:port_conn

        # Datos Recibidos de Server Nombre TLDs
        self._data_name_tlds: list[str] = []  # 0:Dominio 1:TTL 2:Clase 3:Tipo 4:IP_ADDR 5:Puerto

        # Datos Recibidos de Server Nombre Autorativo
        self._data_name_autorativo: list[str] = []

        # Datos a enviar al usuario
        self._dominio: str = ''
        self._clase: str = ''
        self._tipo: str = ''
        self._ip_real: str = ''
        self._error: str = ''
        return

    @property
    def error(self) -> str:
        return self._error

    def enviar_mensaje(self, msg: str) -> None:
        aux: bytes = str.encode(msg)
        self._conn.sendto(aux, self._addr)
        return

    def consulta_cache(self) -> bool:
        if (self._dominio == '') and (self._clase == '') and (self._tipo == '') and (self._ip_real == ''):
            return True
        else:
            return False

    def revisar_url(self) -> bool:
        url: str = self._url
        try:
            dir_aux: list[str] = url.split(sep='://', maxsplit=1)
            if (dir_aux[0] == 'http') or (dir_aux[0] == 'https'):
                aux: list[str] = dir_aux[1].split(sep='.', maxsplit=3)
                self._url_div = aux
                return True
            else:
                return False
        except Exception as e:
            print(e)
            print(f'Ruta mal resivida')
            self._error = 'Error: La URL esta mal escrita y no se puede encontrar'
            return False

    def mensaje_resolver(self) -> str:
        mensaje: str = self._dominio.ljust(30)
        mensaje += self._clase.ljust(5)
        mensaje += self._tipo.ljust(10)
        mensaje += self._ip_real.ljust(20)
        return mensaje

    def _create_list_root(self, data: bytes) -> bool:
        data_str: str = data.decode('utf-8')
        try:
            self._data_root = data_str.split(sep=', ', maxsplit=4)
            if len(self._data_root) == 5:
                return True
            else:
                self._error = data_str
                return False
        except Exception as e:
            print(e)
            self._error = f'Error al recibir los datos: {data_str}'
            return False

    def consulta_server_raiz(self, host: str, port: int) -> bool:
        print('Consulta Servidor Root DNS'.center(50, '-'))
        root_edo: bool
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPConsultaRaiz:
            # Enviando  mensaje al servidor usando el socket UDP
            UDPConsultaRaiz.sendto(str.encode(f'.{self._url_div[2]}'), (host, port))
            root_rcv: bytes = b''
            while root_rcv == b'':
                root_rcv, root_addr = UDPConsultaRaiz.recvfrom(1024)
            if self._create_list_root(root_rcv):
                root_edo = True
            else:
                root_edo = False
        return root_edo

    def _create_list_name_tld(self, data: bytes) -> bool:
        data_str: str = data.decode('utf-8')
        try:
            self._data_name_tlds = data_str.split(sep=', ', maxsplit=5)
            if len(self._data_name_tlds) == 6:
                return True
            else:
                self._error = data_str
                return False
        except Exception as e:
            print(e)
            self._error = f'Error al recibir los datos de TLD: {data_str}'
            return False

    def consulta_server_name_tld(self) -> bool:
        tld_edo: bool
        tld_host: str = str(self._data_root[3])
        tld_port: int = int(self._data_root[4])
        tld_consulta: str = f'{ self._url_div[1] }.{ self._url_div[2] }'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPConsultaTLD:
            UDPConsultaTLD.sendto(str.encode(tld_consulta), (tld_host, tld_port))
            tld_rcv: bytes = b''
            while tld_rcv == b'':
                tld_rcv, tld_addr = UDPConsultaTLD.recvfrom(1024)
            if self._create_list_name_tld(tld_rcv):
                tld_edo = True
            else:
                tld_edo = False
        return tld_edo

    def _create_list_zone(self, data: bytes) -> bool:
        data_str: str = data.decode('utf-8')
        try:
            self._data_name_autorativo = data_str.split(sep=', ', maxsplit=3)
            if len(self._data_name_autorativo) == 4:
                self._dominio = self._data_name_autorativo[0]
                self._clase = self._data_name_autorativo[1]
                self._tipo = self._data_name_autorativo[2]
                self._ip_real = self._data_name_autorativo[3]
                return True
            else:
                self._error = data_str
                return False
        except Exception as e:
            print(e)
            self._error = 'Hubun error al dividir los datos de name'
            return False

    def consulta_server_name_autor(self) -> bool:
        zone_edo: bool
        zone_host: str = str(self._data_name_tlds[4])
        zone_port: int = int(self._data_name_tlds[5])
        zone_consulta: str = f'{self._url_div[1]}.{self._url_div[2]}'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPCosnultaZone:
            UDPCosnultaZone.sendto(str.encode(zone_consulta), (zone_host, zone_port))
            zone_rcv: bytes = b''
            while zone_rcv == b'':
                zone_rcv, zone_addr = UDPCosnultaZone.recvfrom(1024)
            if self._create_list_zone(zone_rcv):
                zone_edo = True
            else:
                zone_edo = False
        return zone_edo


def consulta_resolver(conn: socket.socket, url_rcv: str, name: str, addr) -> None:
    print(f'Iniciando Nuevo Hilo [{ name }]...')
    global LIST_THREAD
    resolver: Resolver = Resolver(url_rcv, conn, addr)
    flag: bool = True
    while flag:
        if resolver.consulta_cache():
            if resolver.revisar_url():
                if resolver.consulta_server_raiz('192.168.0.8', 5555):
                    if resolver.consulta_server_name_tld():
                        if resolver.consulta_server_name_autor():
                            msg: str = resolver.mensaje_resolver()
                            resolver.enviar_mensaje(msg)
                        else:
                            resolver.enviar_mensaje(resolver.error)
                    else:
                        resolver.enviar_mensaje(resolver.error)
                        flag = False
                        continue
                else:
                    resolver.enviar_mensaje(resolver.error)
                    flag = False
                    continue
            else:
                resolver.enviar_mensaje(resolver.error)
                flag = False
                continue
        else:
            resolver.enviar_mensaje(resolver.mensaje_resolver())
            flag = False
    print(f'Terminando ejecucion del hilo: { name }')
    LIST_ADDR.remove(addr)
    LIST_THREAD.remove(threading.currentThread())
    return


if __name__ == '__main__':
    print('Servidor Resolver'.center(100, '-'))
    nhost: str = socket.gethostbyname(socket.gethostname())
    nport: int = 4444
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
        UDPServerSocket.bind((nhost, nport))
        print(f"Servidor UDP Resolver[{nhost}:{nport}]activo, esperando peticiones")
        # Listen for incoming datagrams
        while True:
            url_r, address = UDPServerSocket.recvfrom(1024)
            if url_r != b'':
                LIST_ADDR.append(address)
                name_thread: str = f'Consulta-{ address }'
                thread_read = threading.Thread(
                    target=consulta_resolver,
                    name=name_thread,
                    args=[UDPServerSocket, url_r.decode('utf-8'), name_thread, address]
                )
                # consulta_resolver(UDPServerSocket, url_r.decode('utf-8'), address)
                LIST_THREAD.append(thread_read)
                thread_read.start()
    # print('Fin Prueba Servidor Resolver'.center(100, '-'))
