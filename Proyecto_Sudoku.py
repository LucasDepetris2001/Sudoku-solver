import numpy as np
from pulp import *

##################################################################################################
'''
PROGRAMACIÓN LINEAL
'''
##################################################################################################


def enlistar(A):
    h = []
    for i in range(9):
        for j in range(9):
            for v in range(1, 10):
                if A[i][j] == v:
                    h.append([str(v), str(i), str(j)])
    return h



def generar_matriz(diccionario):
    filas = [str(i) for i in range(9)]
    columnas = [str(i) for i in range(9)]
    valores = [str(i) for i in range(1, 10)]
    A = np.zeros([9, 9], dtype=int)
    for i in filas:
        for j in columnas:
            for v in valores:
                if value(diccionario[v][i][j]) == 1:
                    A[int(i)][int(j)] = int(v)
    return A



def sudoku_lp(A):
    filas = [str(i) for i in range(9)]
    columnas = [str(i) for i in range(9)]
    valores = [str(i) for i in range(1,10)]
    diccionario = LpVariable.dicts('elección', (valores, filas, columnas), 0, 1, LpInteger)
    problema = LpProblem('Problema_Sudoku', LpMinimize)
    problema += 0
    for f in filas:
        for c in columnas:
            problema += lpSum([diccionario[v][f][c] for v in valores]) == 1
    for v in valores:
        for f in filas:
            problema += lpSum([diccionario[v][f][c] for c in columnas]) == 1
    for v in valores:
        for c in columnas:
            problema += lpSum([diccionario[v][f][c] for f in filas]) == 1
    bloques = []
    for i in range(3):
        for j in range(3):
            bloques += [[(filas[3 * i + k], columnas[3 * j + l]) for k in range(3) for l in range(3)]]
    for v in valores:
        for b in bloques:
            problema += lpSum([diccionario[v][f][c] for (f, c) in b]) == 1
    lista = enlistar(A)
    for num in lista:
        problema += diccionario[num[0]][num[1]][num[2]] == 1
    problema.solve(PULP_CBC_CMD(msg=False))
    return generar_matriz(diccionario)




##################################################################################################
'''
BACKTRACKING
'''
##################################################################################################



def factible(A, I, n):
    for k in range(9):
        if A[k][I[1]] == n or A[I[0]][k] == n :
            return False
    caja0 = I[0] // 3
    caja1 = I[1] // 3
    for i in range(caja0 * 3, caja0 * 3 + 3):
        for j in range(caja1 * 3, caja1 * 3 + 3):
            if A[i][j] == n:
                return False
    return True



def sudoku_bt(A):
    for j in range(9):
        for i in range(9):
            if A[i][j] == 0:
                for n in range(1,10):
                    if factible(A, [i,j], n):
                        A[i][j] = n
                        sudoku_bt(A)
                        A[i][j] = 0
                return
    print(np.array(A))










