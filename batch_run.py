import csv
import random
import time
from modelo import MalhaComputacionalModel

def executar_simulacao_larga_escala(semente_inicio=1, semente_fim=100000):
    total_simulacoes = semente_fim - semente_inicio + 1
    nome_arquivo = "resultados_poc_larga_escala.csv"
    total_ciclos = 100

    print("=====================================================================")
    print(f"   INICIANDO SIMULAÇÃO - {total_simulacoes} SEEDS")
    print("=====================================================================")
    print(f"-> Gerando arquivo: {nome_arquivo}\n")
    
    tempo_inicial = time.time()

    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(["Seed", "Perdas_Rigido", "Perdas_Bio_Inspirado", "Reducao_Percentual"])

        for seed in range(semente_inicio, semente_fim + 1):
            
            # Cenário A
            random.seed(seed)
            modelo_tradicional = MalhaComputacionalModel(anastomose_ativa=False)
            for _ in range(total_ciclos):
                modelo_tradicional.step()
            perdas_A = modelo_tradicional.obter_total_perdas()

            # Cenário B
            random.seed(seed)
            modelo_simbiotico = MalhaComputacionalModel(anastomose_ativa=True)
            for _ in range(total_ciclos):
                modelo_simbiotico.step()
            perdas_B = modelo_simbiotico.obter_total_perdas()

            # Cálculos
            reducao = ((perdas_A - perdas_B) / perdas_A * 100) if perdas_A > 0 else 0.0

            escritor.writerow([seed, perdas_A, perdas_B, round(reducao, 2)])

            if seed % 10000 == 0:
                print(f" Progresso: {seed}/{semente_fim} sementes processadas... Tempo: {time.time() - tempo_inicial:.1f}s")

    print(f"\nConcluído! Tempo total de processamento: {time.time() - tempo_inicial:.2f}s")

if __name__ == "__main__":
    executar_simulacao_larga_escala(1, 100000)