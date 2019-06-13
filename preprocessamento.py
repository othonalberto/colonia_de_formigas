import numpy as np
from pandas import *

np.set_printoptions(precision=6)
nome = 'Luxemburgo'

arquivo = open('arquivos/' + nome + '.txt')
nLinhas = int(arquivo.readline())

matriz = np.zeros((nLinhas, 3))
matrizDistancias = np.zeros((nLinhas, nLinhas))

i = 0

for linhaPrincipal in arquivo:    
    separadosPrincipal = linhaPrincipal.split(" ")
    separadosPrincipal[2] = separadosPrincipal[2].rstrip()

    for j in range(0, len(separadosPrincipal)):
        separadosPrincipal[j] = float(separadosPrincipal[j])

    matriz[i] = separadosPrincipal

    i += 1


for linhaPrincipal in matriz:    
    nomei = linhaPrincipal[0]
    xi    = linhaPrincipal[1]
    yi    = linhaPrincipal[2]

    for linhaSecundaria in matriz:
        nomej = linhaSecundaria[0]
        xj    = linhaSecundaria[1]
        yj    = linhaSecundaria[2]

        indexi = int(nomei) - 1
        indexj = int(nomej) - 1
        
        if (nomei == nomej):
            matrizDistancias[indexi][indexj] = 0
        else:
            matrizDistancias[indexi][indexj] = np.sqrt((xi-xj)**2 + (yi - yj)**2)

df = (DataFrame(matrizDistancias))
    
df.to_csv('arquivos/saida_' + nome + '.csv', sep=' ', header=False, float_format='%.6f', index=False)

print(DataFrame(df))
"""
As linhas abaixo importam o arquivo csv como uma matriz e printa na tela
"""

# matrixteste = np.loadtxt(open("arquivos/saida_djibout.csv", "rb"), delimiter=" ", skiprows=0)
# print(DataFrame(matrixteste))