import random
# import os


class Buscaminas:
    def __init__(self, dificultad: int):
        self.__dificultad: int = dificultad
        self.__coorEjeX: int = 0
        self.__coorEjeY: int = 0
        self.__mapa: None
        self.__mapaMinas: None
        self.__puntaje: int = 0
        if self.__dificultad == 1:
            # 1: Principiante
            self.__mapa = [
                ['M', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],  # Fila 0
                ['1', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 1
                ['2', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 2
                ['3', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 3
                ['4', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 4
                ['5', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 5
                ['6', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 6
                ['7', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 7
                ['8', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 8
                ['9', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 9
            ]
            self.__mapaMinas = [
                ['M', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],  # Fila 0
                ['1', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 1
                ['2', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 2
                ['3', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 3
                ['4', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 4
                ['5', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 5
                ['6', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 6
                ['7', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 7
                ['8', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 8
                ['9', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 9
            ]
            minas = 0
            while minas < 10:
                eje_x = random.randrange(1, 9)
                eje_y = random.randrange(1, 9)
                if self.__mapaMinas[eje_y][eje_x] == 'X':
                    continue
                else:
                    self.__mapaMinas[eje_y][eje_x] = 'X'
                    minas += 1

        elif self.__dificultad == 2:
            # 2: Avanzado
            self.__mapa = [
                ['BM', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],  # Fila CoorX
                ['01', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 1
                ['02', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 2
                ['03', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 3
                ['04', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 4
                ['05', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 5
                ['06', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 6
                ['07', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 7
                ['08', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 8
                ['09', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 9
                ['10', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 10
                ['11', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 11
                ['12', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 12
                ['13', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 13
                ['14', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 14
                ['15', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 15
                ['16', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 16
            ]
            self.__mapaMinas = [
                ['BM', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],  # Fila CoorX
                ['01', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 1
                ['02', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 2
                ['03', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 3
                ['04', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 4
                ['05', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 5
                ['06', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 6
                ['07', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 7
                ['08', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 8
                ['09', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 9
                ['10', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 10
                ['11', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 11
                ['12', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 12
                ['13', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 13
                ['14', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 14
                ['15', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 15
                ['16', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Fila 16
            ]
            minas = 0
            while minas < 40:
                eje_x = random.randrange(1, 16)
                eje_y = random.randrange(1, 16)
                if self.__mapaMinas[eje_y][eje_x] == 'X':
                    continue
                else:
                    self.__mapaMinas[eje_y][eje_x] = 'X'
                    minas += 1

    def imprimir_mapa(self) -> str:
        imprimir = 'Buscaminas:\n'
        for filas in self.__mapa:
            for columna in filas:
                imprimir += columna + ' '
            imprimir += '\n'
        return imprimir

    def imprimir_mapa_minas(self) -> str:
        imprimir = ''
        for filas in self.__mapaMinas:
            for columna in filas:
                imprimir += columna + ' '
            imprimir += '\n'
        return imprimir

    def in_coor(self, x: int, y: int) -> bool:
        if x == 0 or y == 0:
            return False
        elif self.__dificultad == 1 and (x > 9 or y > 9):
            return False
        elif self.__dificultad == 2 and (x > 16 or y > 16):
            return False
        else:
            self.__coorEjeX = x
            self.__coorEjeY = y
            return True

    def jugar_new_coor(self):
        x = self.__coorEjeX
        y = self.__coorEjeY
        if self.__mapaMinas[y][x] == 'X':
            fila = 0
            columna = 0
            if self.__dificultad == 1:
                total = 9
            else:
                total = 16
            while fila < total:
                while columna < total:
                    if self.__mapaMinas[fila + 1][columna + 1] == 'X':
                        self.__mapa[fila + 1][columna + 1] = 'X'
                    columna += 1
                columna = 0
                fila += 1
            return False
        else:
            self.__mapa[y][x] = 'O'
            self.__puntaje += 1
            return True

    def state_juego(self):
        if (self.__dificultad == 1) and (self.__puntaje == 71):
            return True
        elif (self.__dificultad == 2) and (self.__puntaje == 216):
            return True
        else:
            return False

    @property
    def puntaje(self):
        return self.__puntaje

    def dificultad(self):
        return self.__dificultad


"""
def clear_console():
    command = 'cls'
    # if os.name in ('nt', 'dos'): # Si la maquina esta corriendo Windows usara cls
    #    command = 'cls'
    os.system(command)
"""
"""
print('INICIO DEL JUEGO')
juego1 = Buscaminas(1)
print('Buscaminas:')
juego = True
while juego:
    clear_console()
    print(juego1.imprimir_mapa())
    x = int(input('Introduce Columna(eje x): '))
    y = int(input('Introduce Fila(eje y): '))
    juego = juego1.in_coor(x, y)
    if not juego:
        print(f'Error en las coordenadas introucidas ({x},{y})')
        continue
    juego = juego1.jugar_new_coor()
    if not juego:
        clear_console()
        print(f'Has perdido')
        print(juego1.imprimir_mapa())
        continue

print(juego1.imprimir_mapa())
print(f'Mapa con minas: \n {juego1.imprimir_mapa_minas()}')

juego2 = Buscaminas(2)
print('Buscaminas:')
print(juego2.imprimir_mapa())
print(f'Mapa con minas: \n {juego2.imprimir_mapa_minas()}')
"""