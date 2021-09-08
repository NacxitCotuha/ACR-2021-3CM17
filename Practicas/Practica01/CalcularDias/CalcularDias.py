# Algoritmo para calcular los dias que he vivido hasta el 26 de agosto del 2021

print("PROGRAMA PARA CALCULAR LOS DIAS VIVIDO HASTA EL 26 DE AGOSTO DEL 2021")
fechaBase: tuple[int, int, int] = (26, 8, 2021)  # (dd, mm, aa) = 04/02/2020
meses = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def comprobar_fecha(dia: int, mes: int, anio: int) -> bool:
    if (anio == fechaBase[2]) and (mes <= fechaBase[1]):
        if dia < fechaBase[0] and (mes == fechaBase[1]):
            return True
        elif (dia <= meses[mes - 1]) and (mes < fechaBase[1]):
            return True
        else:
            return False
    elif (anio <= fechaBase[2]) and (0 < mes <= 12):
        fil1 = (0 < dia <= meses[mes - 1] and mes != 2)
        aux_f1 = (anio % 4 == 0) and (0 < dia <= meses[mes - 1])
        aux_f2 = (anio % 4 != 0) and (0 < dia <= meses[mes - 1] - 1)
        fil2 = mes == 2 and (aux_f1 or aux_f2)
        if fil1 or fil2:
            return True
        else:
            return False
    else:
        return False


def sumar_dias(dia_i: int, dia_v: int) -> int:
    return dia_v - dia_i


def sumar_meses(dia: int, mes: int, mes_v: int, anio) -> int:
    res_m = 0
    while mes < mes_v:
        if mes_v == 2:
            if anio % 4 == 0:
                res_m += meses[mes_v - 1]
            else:
                res_m += meses[mes_v - 1] - 1
        else:
            res_m += meses[mes_v - 1]
        mes_v -= 1
    else:
        if mes_v == 2:
            if anio % 4 == 0:
                res_m += sumar_dias(dia, meses[mes_v - 1])
            else:
                res_m += sumar_dias(dia, meses[mes_v - 1] - 1)
        else:
            res_m += sumar_dias(dia, meses[mes_v - 1])
    return res_m


def calcular_total_dias(dia, mes, anio) -> int:
    aux_a = fechaBase[2]
    if anio == fechaBase[2]:
        if mes == fechaBase[1]:
            total = sumar_dias(dia, fechaBase[0])
        else:
            total = fechaBase[0]
            total += sumar_meses(dia, mes, fechaBase[1] - 1, fechaBase[2])
    else:
        total = fechaBase[0] + sumar_meses(0, 1, fechaBase[1] - 1, fechaBase[2])
        aux_a -= 1
        while anio < aux_a:
            if aux_a % 4 == 0:
                total += 366
            else:
                total += 365
            aux_a -= 1
        else:
            total += sumar_meses(dia, mes, 12, anio)
    return total


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


print("Ingresa fecha de nacimiento(dd/mm/aaaa): ")
diaNac = int(input("Dia(int)(dd): "))
mesNac = int(input("Mes(int)(mm): "))
anioNac = int(input("Año(int)(aaaa): "))

if comprobar_fecha(diaNac, mesNac, anioNac):
    print(f'\nFecha ingresada (dd/mm/aaaa): {diaNac}/{mesNac}/{anioNac}')
    totalDias = calcular_total_dias(diaNac, mesNac, anioNac)
    print(f'Numero total de dias vividos hasta el {fechaBase[0]}/{fechaBase[1]}/{fechaBase[2]} = {totalDias}')
    practica1(totalDias)
else:
    print(f'\nLo Sentimos pero posiblemente este mal tu fecha')
    print(f'Fecha ingresada: {diaNac}/{mesNac}/{anioNac}')
print('Fin del programa')
