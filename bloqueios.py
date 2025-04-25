import random

def gerar_restricoes_tabuleiro(tamanho_tabuleiro, semente_aleatoria=42):
    # Gera posições aleatórias no tabuleiro onde rainhas não podem ser colocadas
    random.seed(semente_aleatoria)  
    total_casas = tamanho_tabuleiro ** 2

    # Define intervalo de 7% a 13% do total de casas para bloqueios
    limite_inferior = int(0.07 * total_casas)
    limite_superior = int(0.13 * total_casas)

    # Sorteia a quantidade exata de bloqueios dentro do intervalo
    num_bloqueios = random.randint(limite_inferior, limite_superior)

    posicoes_bloqueadas = set()

    # Gera posições únicas até atingir a quantidade de bloqueios
    while len(posicoes_bloqueadas) < num_bloqueios:
        linha = random.randrange(tamanho_tabuleiro)
        coluna = random.randrange(tamanho_tabuleiro)
        posicoes_bloqueadas.add((linha, coluna))  # Adiciona par (linha, coluna)

    return posicoes_bloqueadas

def imprimir_tabuleiro(dimensao, rainhas_posicionadas, casas_bloqueadas):
    # Cria uma matriz visual do tabuleiro
    tabuleiro_visual = [["." for _ in range(dimensao)] for _ in range(dimensao)]

    # Marca as posições bloqueadas com "X"
    for linha, coluna in casas_bloqueadas:
        tabuleiro_visual[linha][coluna] = "X"

    # Adiciona as rainhas na matriz com "♛"
    if isinstance(rainhas_posicionadas[0], int):
        for linha_idx, coluna_rainha in enumerate(rainhas_posicionadas):
            tabuleiro_visual[linha_idx][coluna_rainha] = "♛"
    else:
        for linha_idx, coluna_idx in rainhas_posicionadas:
            tabuleiro_visual[linha_idx][coluna_idx] = "♛"

    # Imprime o tabuleiro linha por linha
    for linha in tabuleiro_visual:
        print(" ".join(linha))
