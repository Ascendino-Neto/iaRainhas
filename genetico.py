import random
import time

# Avalia o número de conflitos entre rainhas e bloqueios
def avaliar(individuo, bloqueios):
    conflitos = 0
    n = len(individuo)
    for i in range(n):
        for j in range(i + 1, n):
            # Verifica conflitos na mesma coluna ou diagonais
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
        # Verifica se a posição está bloqueada
        if (i, individuo[i]) in bloqueios:
            conflitos += 1
    return conflitos

# Gera um indivíduo aleatório com uma permutação de colunas
def gerar_individuo(n):
    individuo = list(range(n))
    random.shuffle(individuo)
    return individuo

# Seleciona os melhores indivíduos com base na avaliação (menor é melhor)
def selecao(populacao, bloqueios):
    # Ordena por avaliação (número de conflitos)
    return sorted(populacao, key=lambda x: avaliar(x, bloqueios))

# Realiza o cruzamento entre dois pais para gerar um filho
def cruzar(pai1, pai2):
    n = len(pai1)
    ponto = random.randint(0, n - 1)
    filho = pai1[:ponto] + [g for g in pai2 if g not in pai1[:ponto]]
    return filho

# Aplica mutação trocando duas posições aleatórias
def mutar(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

# Executa o algoritmo genético
def resolver_com_genetico(n, bloqueios, max_geracoes=1000, tam_populacao=100, taxa_mutacao=0.1):
    populacao = [gerar_individuo(n) for _ in range(tam_populacao)]  # Geração inicial
    melhor_avaliacao = float('inf')
    soma_avaliacoes = 0
    total_nos = 0

    inicio = time.time()

    for geracao in range(max_geracoes):
        populacao = selecao(populacao, bloqueios)  # Ordena pela qualidade
        nova_populacao = []

        for _ in range(tam_populacao):
            pai1, pai2 = random.sample(populacao[:50], 2)  # Seleção dos pais
            filho = cruzar(pai1, pai2)  # Crossover
            filho = mutar(filho, taxa_mutacao)  # Mutação
            nova_populacao.append(filho)

        populacao = nova_populacao
        total_nos += tam_populacao

        avaliacoes = [avaliar(ind, bloqueios) for ind in populacao]
        melhor_geracao = min(avaliacoes)
        soma_avaliacoes += sum(avaliacoes)

        # Se encontrou uma solução perfeita, retorna
        if melhor_geracao == 0:
            fim = time.time()
            melhor_individuo = populacao[avaliacoes.index(0)]
            return {
                "solucao": melhor_individuo,
                "tempo": fim - inicio,
                "nos": total_nos,
                "melhor_avaliacao": 0,
                "media_avaliacao": soma_avaliacoes / ((geracao + 1) * tam_populacao)
            }

    fim = time.time()
    melhor_individuo = min(populacao, key=lambda x: avaliar(x, bloqueios))
    melhor_avaliacao = avaliar(melhor_individuo, bloqueios)

    return {
        "solucao": None if melhor_avaliacao > 0 else melhor_individuo,
        "tempo": fim - inicio,
        "nos": total_nos,
        "melhor_avaliacao": melhor_avaliacao,
        "media_avaliacao": soma_avaliacoes / (max_geracoes * tam_populacao)
    }

