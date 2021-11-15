import socket
import sys

from FTPClient import FTPClient, in_data

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'Usar: { sys.argv } <HOST> <PORT> <PORT_TRANSFER>')
        sys.exit(1)
    try:
        host: str = sys.argv[1]
        port: int = int(sys.argv[2])
        port_transfer: int = int(sys.argv[3])
    except Exception as e:
        print(e)
        print(f'Usar: { sys.argv } <HOST: str> <PORT: int> <PORT_TRANSFER: int>')
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        TCPClientSocket.connect((host, port))
        ftp_client: FTPClient = FTPClient(TCPClientSocket, 'Servidor FTP/TCP')
        msg_rcv: str = ftp_client.recibir_mensajes()
        msg_env: str = ''
        print(msg_rcv)
        if ftp_client.validacion():
            print(f'Acceso aceptado por [{ftp_client.nombre}]...')
            while msg_env != 'QUIT':
                msg_rcv = ftp_client.recibir_mensajes()
                print('\n', msg_rcv)
                msg_env = in_data('Archivo a descargar: ')
                ftp_client.enviar_menssaje(msg_env)
                ftp_client.transferencia_archivo(msg_env, port_transfer)
                msg_env = in_data('Para Salir escribir QUIT: ')
                if msg_env == 'QUIT':
                    ftp_client.enviar_menssaje(msg_env)
                    continue
                else:
                    msg_env = 'CONTINUE'
                    ftp_client.enviar_menssaje(msg_env)
                    continue
        else:
            print(f'Acceso denegado por [{ftp_client.nombre}]...')
