import random
import time

# Avalia a qualidade de uma solução, penalizando conflitos e bloqueios
def avaliar_posicao(individuo, tamanho, bloqueios):
    penalidades = 0
    for i in range(tamanho):
        if (i, individuo[i]) in bloqueios:
            penalidades += 1  # Penaliza se a posição está bloqueada
        for j in range(i + 1, tamanho):
            mesma_coluna = individuo[i] == individuo[j]
            mesma_diagonal = abs(individuo[i] - individuo[j]) == abs(i - j)
            if mesma_coluna or mesma_diagonal:
                penalidades += 1  # Penaliza conflitos entre rainhas
    return -penalidades

# Cria uma população inicial de indivíduos aleatórios (sem repetições por linha)
def criar_populacao(qtd_individuos, tamanho):
    return [random.sample(range(tamanho), tamanho) for _ in range(qtd_individuos)]

# Seleciona dois pais por torneio (amostragem de 5 e escolhe os melhores)
def torneio_selecao(populacao, avaliacoes):
    amostra = random.sample(list(zip(populacao, avaliacoes)), 5)
    amostra.sort(key=lambda x: x[1], reverse=True)
    return amostra[0][0], amostra[1][0]

# Realiza o cruzamento ordenado entre dois pais
def cruzar(pai_a, pai_b, tamanho):
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho = [-1] * tamanho
    filho[inicio:fim] = pai_a[inicio:fim]  # Copia segmento do primeiro pai

    idx = fim
    for gene in pai_b:
        if gene not in filho:
            while filho[idx % tamanho] != -1:
                idx += 1
            filho[idx % tamanho] = gene  # Preenche o restante com o segundo pai
    return filho

# Aplica uma mutação por troca de posições com certa probabilidade
def aplicar_mutacao(individuo, prob, tamanho):
    if random.random() < prob:
        i, j = random.sample(range(tamanho), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

# Usa backtracking para tentar completar uma solução parcialmente boa
def completar_solucao_base(base_inicial, tamanho, bloqueios):
    def posicao_permitida(tabuleiro, linha, coluna):
        if (linha, coluna) in bloqueios:
            return False
        for i in range(linha):
            mesma_col = tabuleiro[i] == coluna
            mesma_diag = abs(tabuleiro[i] - coluna) == abs(i - linha)
            if mesma_col or mesma_diag:
                return False
        return True

    def tentar_completar(tabuleiro, linha):
        if linha == tamanho:
            return tabuleiro
        for col in range(tamanho):
            if posicao_permitida(tabuleiro, linha, col):
                tabuleiro[linha] = col
                resultado = tentar_completar(tabuleiro, linha + 1)
                if resultado:
                    return resultado
        return None

    copia_base = base_inicial[:]
    return tentar_completar(copia_base, len(base_inicial))

# Algoritmo genético completo com etapas de seleção, cruzamento, mutação e reparo
def resolver_por_genetico(tamanho_tabuleiro, casas_bloqueadas, qtd_pop=1000, limite_geracoes=5000, taxa_mutacao=0.3):
    inicio_execucao = time.time()
    populacao = criar_populacao(qtd_pop, tamanho_tabuleiro)
    avaliacoes = [avaliar_posicao(ind, tamanho_tabuleiro, casas_bloqueadas) for ind in populacao]
    total_avaliacoes = qtd_pop

    for _ in range(limite_geracoes):
        nova_geracao = []
        for _ in range(qtd_pop // 2):
            p1, p2 = torneio_selecao(populacao, avaliacoes)
            f1 = aplicar_mutacao(cruzar(p1, p2, tamanho_tabuleiro), taxa_mutacao, tamanho_tabuleiro)
            f2 = aplicar_mutacao(cruzar(p2, p1, tamanho_tabuleiro), taxa_mutacao, tamanho_tabuleiro)
            nova_geracao.extend([f1, f2])

        populacao = nova_geracao
        avaliacoes = [avaliar_posicao(ind, tamanho_tabuleiro, casas_bloqueadas) for ind in populacao]
        total_avaliacoes += qtd_pop

        # Verifica se há solução perfeita (sem penalidades)
        for idx, score in enumerate(avaliacoes):
            if score == 0:
                fim_execucao = time.time()
                return {
                    "solucao": populacao[idx],
                    "tempo": fim_execucao - inicio_execucao,
                    "nos_avaliados": total_avaliacoes,
                    "melhor_pontuacao": max(avaliacoes),
                    "media_populacao": sum(avaliacoes) / len(avaliacoes)
                }

    # Tenta recuperar uma solução parcialmente boa com backtracking
    for individuo in populacao:
        if avaliar_posicao(individuo, tamanho_tabuleiro, casas_bloqueadas) > -10:
            tentativa = completar_solucao_base(individuo, tamanho_tabuleiro, casas_bloqueadas)
            if tentativa:
                fim_execucao = time.time()
                return {
                    "solucao": tentativa,
                    "tempo": fim_execucao - inicio_execucao,
                    "nos_avaliados": total_avaliacoes,
                    "melhor_pontuacao": max(avaliacoes),
                    "media_populacao": sum(avaliacoes) / len(avaliacoes)
                }

    # Retorna falha caso nenhuma solução válida tenha sido encontrada
    fim_execucao = time.time()
    return {
        "solucao": None,
        "tempo": fim_execucao - inicio_execucao,
        "nos_avaliados": total_avaliacoes,
        "melhor_pontuacao": max(avaliacoes),
        "media_populacao": sum(avaliacoes) / len(avaliacoes)
    }
