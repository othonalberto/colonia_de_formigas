import numpy as np
from pandas import DataFrame

class Formiga:
    def __init__(self):
        self.tabu = []
        self.rota = []

class Objeto:
    def __init__(self, cidadeA, cidadeB, probabilidade, pf, feromonio, distancia):
        self.cidadeA = cidadeA
        self.cidadeB = cidadeB
        self.probabilidade = probabilidade
        self.feromonio = feromonio
        self.probabilidadeFinal = pf
        self.custo = distancia
        self.visitado = False

VALORPROBINICIAL = 0.000001

COEFICIENTE_EVAPORACAO = 0.8
Q = 100

matrizADJ = np.zeros((1, 1))
matrizProbabilidades = np.zeros(matrizADJ.shape, Objeto)

def carregaConfiguracoes(mADJ):
    global matrizADJ

    matrizADJ = mADJ


def distancia(A, B):
    return matrizADJ[A][B]


def somaDaLinha(linha):
    soma = 0
    for distancia in linha:
        soma += distancia

    return soma


def inicializaMatrizProbabilidades():
    global matrizProbabilidades

    matrizProbabilidades = np.zeros(matrizADJ.shape, Objeto)

    for i in range(0, len(matrizProbabilidades)):
        for j in range(0, len(matrizProbabilidades)):
            if (matrizADJ[i][j] == 0):
                p = 0
            else:
                p = 1/matrizADJ[i][j]

            matrizProbabilidades[i][j] = Objeto(i, j, p, 0, VALORPROBINICIAL, matrizADJ[i][j])

    for i in range(0, len(matrizADJ)):
        linha = matrizProbabilidades[i]

        somaP = somaTodasProbabilidades(linha)

        for j in range(len(matrizADJ)):
            objeto = matrizProbabilidades[i][j]
            objeto.probabilidadeFinal = (objeto.probabilidade * objeto.feromonio) / somaP
            matrizProbabilidades[i][j] = objeto
            
    return matrizProbabilidades


def somaTodasProbabilidades(linha):
    soma = 0

    for objeto in linha:
        soma += objeto.probabilidade * objeto.feromonio

    return soma


def roleta(linhaAtual, formiga):
    global matrizProbabilidades

    soma = 0
    roda = []

    if (len(formiga.tabu) == 0):
        formiga.tabu.append(matrizProbabilidades[linhaAtual][linhaAtual].cidadeB)
        formiga.rota.append(matrizProbabilidades[linhaAtual][linhaAtual])

    # soma de todos os fitness
    for i in range(0, len(matrizProbabilidades)):
        soma += matrizProbabilidades[linhaAtual][i].probabilidadeFinal

    for i in range(0, len(matrizProbabilidades)):
        roda.append(matrizProbabilidades[linhaAtual][i].probabilidadeFinal / soma)

    while True:
        sorteado = np.random.random()
        acc = 0
        index = -1

        while (acc < sorteado):
            index += 1
            acc = acc + roda[index]

        if (index == -1):
            index = 0

        elemento = matrizProbabilidades[linhaAtual][index]
        
        if (not (elemento.cidadeB in formiga.tabu)):
            formiga.tabu.append(elemento.cidadeB)

            return elemento

def calculaCusto(formiga):
    soma = 0

    for elem in formiga.rota:
        soma += distancia(elem.cidadeA, elem.cidadeB)
        
    return soma

def printaRota(formiga):
    soma = 0

    for elem in formiga.rota:
        soma += distancia(elem.cidadeA, elem.cidadeB)
        print(" -> {} " .format(elem.cidadeB), end='')
    
    print("")

def printaTabu(formiga):
    soma = 0

    for elem in formiga.tabu:
        print(" {} " .format(elem), end='')
    
    print("")

def atualizaFeromonio(formigas):
    global matrizProbabilidades

    for i in range(0, len(matrizProbabilidades)):
        for j in range(0, len(matrizProbabilidades)):
            if (i != j):
                objeto = matrizProbabilidades[i][j]
                rota = [objeto.cidadeA, objeto.cidadeB]
                vetorCusto = []

                for i in range(0, len(formigas)):
                    formiga = formigas[i]
                    for posicao in formiga.rota:
                        if ((posicao.cidadeA == rota[0] and posicao.cidadeB == rota[1]) or (posicao.cidadeB == rota[0] and posicao.cidadeA == rota[1])):
                            vetorCusto.append(Q / calculaCusto(formiga))
                    

                feromonioAtual = (matrizProbabilidades[i][j].feromonio) 
                evaporacao = (1 - COEFICIENTE_EVAPORACAO) * feromonioAtual
                matrizProbabilidades[i][j].feromonio = np.sum(vetorCusto) + evaporacao

    atualizaProbabilidadeFinal()

def atualizaProbabilidadeFinal():
    global matrizProbabilidades

    for i in range(0, len(matrizProbabilidades)):
        linha = matrizProbabilidades[i]

        somaP = somaTodasProbabilidades(linha)

        for j in range(0, len(matrizProbabilidades)):
            matrizProbabilidades[i][j].probabilidadeFinal = (matrizProbabilidades[i][j].probabilidade * matrizProbabilidades[i][j].feromonio) / somaP
    