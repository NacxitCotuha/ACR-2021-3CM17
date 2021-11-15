

if __name__ == '__main__':
    url = input('Ingrese URL: ')

    fin: int = len(url)
    new_url: str = url[fin - 3: fin]
    new_url2: str = url[0:4]
    print(f'URL corto: {new_url}')
    print(f'URL corto inicio: {new_url2}')

    div_str: list[str] = url.split(sep='://', maxsplit=1)
    print(f'Division {div_str[0]}       {div_str[1]}')

    lista0: list[str] = []
    lista1: list[str] = ['s', 'a', 'q']
    print(lista1)
    print(lista0)
    lista0 = lista1
    print(lista0)
