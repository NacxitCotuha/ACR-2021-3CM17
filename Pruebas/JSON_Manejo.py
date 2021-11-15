import json
# import os


if __name__ == '__main__':
    print('Manejo de Archivos json'.center(100, '-'))
    with open('busqueda.json') as file:
        file_json = json.load(file)
        if file_json['Numero'] and file_json['usuarios'] and file_json['Datos']:
            data = file_json['Numero'][0]
            num = data['Numero1'] + 2
            print(num)
            print('Usuarios Existe')
            dato1 = file_json['Datos']['numero']
            dato2 = file_json['Datos']['string']
            print(f'{dato2}: {dato1}')
        else:
            print('Usuarios NO Existen')
    print('Manejo de Archivos json FIN'.center(100, '-'))
