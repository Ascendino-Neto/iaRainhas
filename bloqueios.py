import random

# Gera um conjunto aleatório de bloqueios no tabuleiro
def gerar_bloqueios(n, seed=42):
    random.seed(seed)
    total_posicoes = n * n
    minimo = int(total_posicoes * 0.07)
    maximo = int(total_posicoes * 0.13)
    quantidade = random.randint(minimo, maximo)  # Número aleatório de bloqueios

    bloqueios = set()
    while len(bloqueios) < quantidade:
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        bloqueios.add((i, j))  # Adiciona coordenada bloqueada
    return bloqueios

# Exibe o tabuleiro com as rainhas (Q) e bloqueios (X)
def mostrar_tabuleiro(n, rainhas, bloqueios):
    tabuleiro = [["." for _ in range(n)] for _ in range(n)]  # Inicializa o tabuleiro vazio

    for i, j in bloqueios:
        tabuleiro[i][j] = "X"  # Marca os bloqueios

    # Marca as rainhas no tabuleiro
    if isinstance(rainhas[0], int):  # Representação por coluna
        for linha, coluna in enumerate(rainhas):
            tabuleiro[linha][coluna] = "Q"
    else:  # Representação como lista de pares (linha, coluna)
        for linha, coluna in rainhas:
            tabuleiro[linha][coluna] = "Q"

    for linha in tabuleiro:
        print(" ".join(linha))  # Imprime o tabuleiro
