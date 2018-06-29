#!/usr/local/env python
import math as np
from random import randint, random
from bitstring import BitArray

# Cromossomo: usado para modelar a solucao
#           - eh a solucao do problema
#           - cromossomo = solucao = individuo

''
# Modelagem do problema
# Problema: maximizar o numero de 1s no cromossomo
#   - Precisa definir a funcao de fitness
#   - Precisa definir o fenotipo do cromossomo
def calcula_binario (comeco, tamanho, indice, cromo):
    aux = 0
    for i in range(comeco, tamanho):
        aux += cromo[i] * 2 ** indice
        indice -= 1
    return aux

def fitness(cromossomo: list) -> float:
    # Funcao de fitness: avalia um cromossomo
    # - Deve ser capaz de avaliar se um cromossomo eh melhor que outro
    # - Avalia se a solucao eh boa ou ruim

    # decodificacao do cromossomo
    x0, x1 = decodifica(cromossomo)

    # Para impedir que a populacao convirja rapido
    # e aplicado a penalidade para x0 == x1
    penalidade = 0
    if x0 == x1:
        penalidade = 100

    # Calculo (bascara)
    y0 = x0 ** 2 + 2 * x0 - 3
    y1 = x1 ** 2 + 2 * x1 - 3

    # Soma dos dois Xs e mais a penalidade caso pecise
    return abs(y0) + abs(y1) + penalidade


def decodifica(cromossomo):

    # Extrai o sinal
    sinal_x = cromossomo[0]
    sinal_y = cromossomo[8]

    # Extrai o numero e converte para inteiro
    x = BitArray(cromossomo[1:8]).uint
    y = BitArray(cromossomo[9:16]).uint

    # Aplica o sinal no numero
    if sinal_x == 1: x *= -1
    if sinal_y == 1: y *= -1

    return x, y

def roleta(populacao):
    """
    Implementacao do algoritmo da roleta viciada.
    :param populacao: lista com todos os cromossomos
    :return: lista com os pares de pais que vao cruzar entre si
    """

    # 1. Calcula o total do fitness de todos os cromossomos
    total = 1
    for individuo in populacao:
        total += individuo[1]

    # print(f'total: {total}')
    # print('total: {0}'.format(total)) # equivalente

    # 2. Calcula as porcentagens
    #    print('Calculando as porcentagens: ')
    for individuo in populacao:
        individuo.append(individuo[1] / total)
    # print(individuo)

    # 3. Calcula as porcentagens acumuladas
    #    print('Calculando as porcentagens acumuladas: ')

    anterior = 0
    for individuo in populacao:
        acumulado = anterior + individuo[2]
        individuo.append(acumulado)

        anterior = acumulado
    # print(individuo)

    # 4. Gerar os n pares de pais
    pais = []
    for i in range(int(len(populacao) / 2)):
        roleta1 = random()
        roleta2 = random()

        pai1 = populacao[0][:2]
        pai2 = populacao[0][:2]

        # TODO: Verificar pq a roleta esta quebrando
        for individuo in populacao:
            # print(f'1: {roleta1} - {individuo[3]}')
            if roleta1 <= individuo[3]:
                pai1 = individuo[:2]
                break

        for individuo in populacao:
            # print(f'2: {roleta2} - {individuo[3]} - {populacao}')
            if roleta2 <= individuo[3]:
                pai2 = individuo[:2]
                break

                # TODO: Corrigir a selecao de 2 pais iguais
                #        print(f'>>1 {pai1} ')
                #        print(f'>>2 {pai2} ')
        pais.append([pai1, pai2])

    # print('Lista de pais:')
    #    for individuo in pais:
    #        print(f'{individuo[0][0]} - {individuo[1][0]}')

    return pais

def torneio(populacao):
    #Populacao tamanho
    tamanho_popu = len(populacao)
    #Torneio
    selecionados = []
    #Percorre a populacao
    for j in range(int(len(populacao)/2)):
        # Obtem os pais
        pai0 = populacao[0][:2]
        pai1 = populacao[0][:2]
        #Selesiona quem disputara o torneio
        candidato0 = randint(0, tamanho_popu - 1)
        candidato1 = randint(0, tamanho_popu - 1)
        candidato2 = randint(0, tamanho_popu - 1)
        candidato3 = randint(0, tamanho_popu - 1)
        #Efetua a comparacao entre os candidatos, o maior ganha
        if populacao[candidato3][1] < populacao[candidato0][1]:
            selecionado1 = populacao[candidato3]
        else:
            selecionado1 = populacao[candidato0]
        if populacao[candidato1][1] < populacao[candidato2][1]:
            selecionado2 = populacao[candidato1]
        else:
            selecionado2 = populacao[candidato2]

        selecionados.append([selecionado1, selecionado2])

    return selecionados

def crossover(pais, taxa_mutacao):
    filhos = []

    for par in pais:
        # Extrai os dois pais da lista
        pai1 = par[0][0]
        pai2 = par[1][0]

        # Sorteia o ponto de corte
        corte = randint(0, len(pai1) - 1)

        # Realiza o crossover
        filho1 = pai1[:corte] + pai2[corte:]
        filho2 = pai2[:corte] + pai1[corte:]

        # Aplica a mutacao
        for i in range(0, len(filho1)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                #                print(f'Sofreu mutacao! {probabilidade}')
                #                print(f'antes:  {filho1}')
                filho1[i] = int(not filho1[i])
                #                print(f'depois: {filho1}')

        for i in range(0, len(filho2)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                #                print(f'Sofreu mutacao! {probabilidade}')
                #                print(f'antes:  {filho2}')
                filho2[i] = int(not filho2[i])
                #                print(f'depois: {filho2}')

        # Salva os filhos gerados
        filhos.append([filho1, fitness(filho1)])
        filhos.append([filho2, fitness(filho2)])

        #   print('Filhos gerados: ')
        #   for individuo in filhos:
        #       print(f'{individuo[0]} => {individuo[1]}')

    return filhos

def crossover2corters(pais, taxa_mutacao):
    gerados = []
    for j in pais:
        pai0 = j[0][0]
        tamPai0 = len(pai0)
        pai1 = j[1][0]
        tamPai1 = len(pai1)

        corte0 = []
        corte1 = []

        corteAceito = False

        indicedeCorte1 = None
        indicedeCorte2 = None

        while(corteAceito == False):
            indicedeCorte1 = randint(0, tamPai0 - 1)
            indicedeCorte2 = randint(0, tamPai1 - 1)

            if indicedeCorte1 > 0 and indicedeCorte1 < int(tamPai0 - 1) \
                    and indicedeCorte2 > 0 and indicedeCorte2 < int(tamPai0 - 1) \
                    and indicedeCorte1 != indicedeCorte2 and indicedeCorte1 < indicedeCorte2:
                corteAceito = True

        if indicedeCorte1 < indicedeCorte2:
            for x in range(indicedeCorte1, indicedeCorte2):
                corte0.append(pai0[x])
                corte1.append(pai1[x])

            filho0 = pai0[:indicedeCorte1] + corte1 + pai0[indicedeCorte2:]
            filho1 = pai1[:indicedeCorte1] + corte0 + pai1[indicedeCorte2:]

        for x in range(0, len(filho0)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                filho1[x] = int(not filho1[x])

        for x in range(0, len(filho1)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                filho1[x] = int(not filho1[x])

        gerados.append([filho0, fitness(filho0)])
        gerados.append([filho1, fitness(filho1)])

    return gerados

def crossoverUniforme(pais, taxa_mutacao):
    gerados = []

    for y in pais:
        pai0 = y[0][0]
        pai1 = y[1][0]

        filho = []

        mascara = [randint(0, 1) for j in range(0, len(pai0))]

        for x in mascara:
            if mascara[x] == 1:
                filho.append(pai0[x])
            elif mascara[x] == 0:
                filho.append(pai1[x])

        for x in range(0, len(filho)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                filho[x] = int(not filho[x])

        # Salva os filhos gerados
        gerados.append([filho, fitness(filho)])

    return gerados



def elitismo(populacao, tam_populacao):
    # Ordena pelo fitness
    populacao.sort(key=lambda individuo: individuo[1], reverse=False)

    # Retorna os n primeiros
    return populacao[:tam_populacao]


def algoritmo_genetico(tam_populacao,
                       tam_cromossomo,
                       max_geracoes,
                       taxa_mutacao):
    # Inicializa a populacao
    populacao = [
        [randint(0, 1) for i in range(0, tam_cromossomo)]
        for j in range(0, tam_populacao)
    ]
    print(populacao)

    # Avaliacao dos cromossomos
    nova_populacao = [
        [cromossomo, fitness(cromossomo)]
        for cromossomo in populacao
    ]

    # Geracoes
    geracao = 0

    while geracao < max_geracoes:

        print(f'### GERACAO {geracao} ###')
        nova_populacao.sort(key=lambda individuo: individuo[1], reverse=False)
        print(f'{nova_populacao[0][0]} => {nova_populacao[0][1]}')

        #for individuo in nova_populacao:
        #    print(f'{individuo[0]} => {individuo[1]}')

        # Selecao dos pais
        #pais = roleta(nova_populacao)
        pais = torneio(nova_populacao)

        # Recombinacao (crossover) e mutacao
        # filhos = crossover(pais, taxa_mutacao)
        filhos = crossoverUniforme(pais, taxa_mutacao)
        #filhos = crossover2corters(pais, taxa_mutacao)

        nova_populacao += filhos
        nova_populacao.sort(key=lambda individuo: individuo[1], reverse=False)

        #        print('Populacao total')
        #        for individuo in nova_populacao:
        #            print(f'{individuo[0]} => {individuo[1]}')

        # Selecao dos sobreviventes
        nova_populacao = elitismo(nova_populacao, tam_populacao)

        #        print('Populacao sobrevivente')
        #        for individuo in nova_populacao:
        #            print(f'{individuo[0]} => {individuo[1]}')

        # passa para geracao seguinte
        geracao += 1

        # Retorna a melhor solucao


def main():
    # ----------------------------------
    # Configuracao dos parametros do AG

    # Numero de alelos do cromossomo
    TAM_CROMOSSOMO = 16

    # Tamanho da populacao
    TAM_POPULACAO = 10

    # Numero maximo de geracoes
    MAX_GERACOES = 50

    # Taxa de Mutacao
    TAXA_MUTACAO = 0.01  # 1%

    # Execucao do algoritmo
    algoritmo_genetico(TAM_POPULACAO,
                       TAM_CROMOSSOMO,
                       MAX_GERACOES,
                       TAXA_MUTACAO)

    # Imprime a resposta

    pass


if __name__ == '__main__':
    main()
