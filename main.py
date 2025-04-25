from bloqueios import gerar_restricoes_tabuleiro as gerar_bloqueios, imprimir_tabuleiro as mostrar_tabuleiro
from genetico import resolver_por_genetico as resolver_com_genetico


def mostrar_dados_execucao(n, sucesso, nos, tempo, melhor_avaliacao, media_avaliacao):
    print("\nResumo da Execução:")
    print("+-----------+--------------------+-------------+--------------+----------+----------+")
    print("|  Tamanho  | Solução Encontrada |     Nós     |  Tempo (ms)  |  Melhor  |  Média   |")
    print("+-----------+--------------------+-------------+--------------+----------+----------+")
    print(f"| {n:<9} | {sucesso:<18} | {nos:<11} | {tempo * 1000:<12.2f} | {melhor_avaliacao:<8} | {media_avaliacao:<8.2f} |")
    print("+-----------+--------------------+-------------+--------------+----------+----------+")


def rodar_algoritmo(n):
    restricoes = gerar_bloqueios(n)  # Gera as posições bloqueadas no tabuleiro
    resultado = resolver_com_genetico(n, restricoes)  
    solucao = resultado["solucao"]
    tempo = resultado["tempo"]
    nos = resultado["nos_avaliados"]
    melhor_avaliacao = resultado["melhor_pontuacao"]
    media_avaliacao = resultado["media_populacao"]

    # Determina se a solução foi encontrada ou não
    sucesso = "Sim" if solucao else "Não"

    print(f"\nProcessando n = {n} ...")
    if solucao:
        mostrar_tabuleiro(n, solucao, restricoes)  
    else:
        print("Nenhuma solução válida foi encontrada.")  

    mostrar_dados_execucao(n, sucesso, nos, tempo, melhor_avaliacao, media_avaliacao)  


def main():
    while True:
        print("\n*** N-Rainhas com bloqueios | Algoritmo Genético ***")
        print("0 - Executar para valor único de n")
        print("1 - Executar para faixa de valores")
        escolha = input("Opção desejada (0 ou 1): ").strip()

        if escolha == "0":
            try:
                n = int(input("Digite o valor de n (entre 8 e 512): "))
                if 8 <= n <= 512:
                    rodar_algoritmo(n)  # Executa para o valor de N informado
                else:
                    print("Valor fora do intervalo permitido.")
            except ValueError:
                print("Entrada inválida.")
        elif escolha == "1":
            try:
                ini = int(input("Valor inicial (mínimo 8): "))
                fim = int(input("Valor final (máximo 512): "))
                if ini >= 8 and fim <= 512 and ini <= fim:
                    for n in range(ini, fim + 1):
                        rodar_algoritmo(n)  # Executa para a faixa de valores entre inicio e fim
                else:
                    print("Intervalo inválido.")
            except ValueError:
                print("Entrada inválida.")
        else:
            print("Escolha inválida.")

        if input("\nDeseja executar novamente? (T/F): ").strip().upper() != "T":
            break


if __name__ == "__main__":
    main()  
