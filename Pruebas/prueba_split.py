def main() -> None:
    cadena = input('Ingresar Ruta: ')
    dividir_cadena = cadena.split(sep='/', maxsplit=1024)
    print(f'tamaño de la cadena:{len(dividir_cadena)}')
    for elemento in dividir_cadena:
        print(f'Elemento: [{elemento}]')
    return


if __name__ == '__main__':
    main()
