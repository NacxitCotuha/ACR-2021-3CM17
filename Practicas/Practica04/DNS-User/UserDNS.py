import socket
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usar: { sys.argv } <HOST> <PORT>')
        sys.exit(1)
    try:
        host: str = sys.argv[1]
        port: int = int(sys.argv[2])
    except Exception as e:
        print(e)
        print(f'Usar: { sys.argv } <HOST: str> <PORT: int>')
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPClientDNS:
        # Enviando mensaje al servidor usando el socket UDP
        msg_env: str = input('Ingrese URL (sin espacios): ').strip()
        UDPClientDNS.sendto(str.encode(msg_env), (host, port))
        msg_rb = UDPClientDNS.recvfrom(1024)
        msg_rcv: str = msg_rb[0].decode('utf-8')
        print(f'Respuesta de resolver: \n{msg_rcv}')
