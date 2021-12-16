import os
import platform
import socket

def host_name():
    hname = os.uname()
    print(hname)


def host_name2() -> None:
    print(platform.uname())
    print(platform.node())
    return


def host_name3() -> None:
    print(socket.gethostbyname(socket.gethostname()))
    return


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP: str
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


def main() -> None:
    # host_name()
    host_name2()
    host_name3()
    print(extract_ip())
    return


if __name__ == '__main__':
    main()
