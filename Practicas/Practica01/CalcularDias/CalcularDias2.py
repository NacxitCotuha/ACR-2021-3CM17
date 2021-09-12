import datetime

def practica1(total_dias: int):
    print(f'''
De acuerdo a la operacion R = totalDias % 3 donde las posibles opciones son:
    R = 0 -> Buscaminas
    R = 1 -> Gato Dummy
    R = 2 -> Memoria
Se calculara que opcion te toca...
''')
    print('FELICIDADES')
    if total_dias % 3 == 0:
        print(f'{total_dias} % 3 = 0 te toco BUSCAMINAS')
    elif total_dias % 3 == 1:
        print(f'{total_dias} % 3 = 1 te toco GATO DUMMY')
    elif total_dias % 3 == 2:
        print(f'{total_dias} % 3 = 2 te toco MEMORIA')
    else:
        print(f'{total_dias} % 3 = {total_dias % 3} por lo visto te salvaste de alguna forma :v')


print("PROGRAMA PARA CALCULAR LOS DIAS VIVIDO HASTA EL 26 DE AGOSTO DEL 2021")
destino = datetime.datetime(2021, 8, 26)
dia = int(input('Ingrese dia (int): '))
mes = int(input('Ingrese mes (int): '))
anio = int(input('Ingrese año (int): '))
nac = datetime.datetime(anio, mes, dia)
print(f'Fecha ingresada(YYYY-MM-DD): {nac}')
diasVivido = destino - nac

print(f'Dias total vivido: {diasVivido.days}')
practica1(diasVivido.days)



