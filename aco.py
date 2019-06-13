import numpy as np
from pandas import DataFrame

from functions import *

np.set_printoptions(precision=6)
# nome = 'djibout'
# pathcompleto = 'arquivos/saida_' + nome + ".csv"

matrizADJ = np.loadtxt(open(pathcompleto, "rb"), delimiter=" ", skiprows=0)
matrizFer = np.zeros((len(matrizADJ), len(matrizADJ)))

carregaConfiguracoes(matrizADJ)

QUANTIDADE_FORMIGAS = len(matrizADJ)
MELHOR_SOLUCAO = Formiga()
MELHOR_CUSTO = np.Inf
NITERACOES = 10000

# cria todas as formigas
mi = inicializaMatrizProbabilidades()
for i in range(0, NITERACOES):
    # pega uma rota para cada formiga
    formigas = []
    for j in range(0, QUANTIDADE_FORMIGAS):
        formigas.append(Formiga())

    for x in range(0, QUANTIDADE_FORMIGAS):
        a = formigas[x]

        posicaoInicial = np.random.randint(QUANTIDADE_FORMIGAS)
        primeiro = posicaoInicial

        while (len(a.rota) < len(matrizADJ)-1):
            s = roleta(posicaoInicial, a)
            a.rota.append(s)
            posicaoInicial = s.cidadeB

        a.rota.append(mi[posicaoInicial][primeiro]) # fecha o ciclo

        custoAtual = calculaCusto(a)

        if (custoAtual < MELHOR_CUSTO):
            MELHOR_SOLUCAO = a
            MELHOR_CUSTO = custoAtual
    
    print("[{}] = {}" .format(i, MELHOR_CUSTO ))


print("==========\nMELHOR:")
printaRota(MELHOR_SOLUCAO)
print(calculaCusto(MELHOR_SOLUCAO))
