import random
from modelo import MalhaComputacionalModel

def executar_poc_detalhada(semente=42, ciclos=100):
    print("=====================================================================")
    print(f"       INICIANDO POC {semente})")
    print("=====================================================================\n")

    # --- CENÁRIO A
    print("--- [RUNDOWN] CENÁRIO A: MODELO RÍGIDO ---")
    random.seed(semente)
    modelo_rigido = MalhaComputacionalModel(anastomose_ativa=False)
    
    for ciclo in range(1, ciclos + 1):
        modelo_rigido.step()
        cargas = [a.carga_atual for a in modelo_rigido.agents]
        perdas_acumuladas = sum([a.requisicoes_perdidas for a in modelo_rigido.agents])
        print(f"Ciclo {ciclo:03d} | Cargas Injetadas (Nós 0-3): {cargas} | Perdas Acumuladas: {perdas_acumuladas} u.c.")

    perdas_rigido = sum([a.requisicoes_perdidas for a in modelo_rigido.agents])

    print("\n" + "="*70 + "\n")

    # --- CENÁRIO B
    print("--- [RUNDOWN] CENÁRIO B: MODELO BIO-INSPIRADO---")
    random.seed(semente)
    modelo_bio = MalhaComputacionalModel(anastomose_ativa=True)

    for ciclo in range(1, ciclos + 1):
        modelo_bio.step()
        cargas = [a.carga_atual for a in modelo_bio.agents]
        perdas_acumuladas = sum([a.requisicoes_perdidas for a in modelo_bio.agents])
        print(f"Ciclo {ciclo:03d} | Cargas Injetadas (Nós 0-3): {cargas} | Perdas Acumuladas: {perdas_acumuladas} u.c.")

    perdas_bio = sum([a.requisicoes_perdidas for a in modelo_bio.agents])

    print("\n=====================================================================")
    print("                          RESULTADOS                              ")
    print("=====================================================================")
    print(f"Perdas Modelo Rígido:        {perdas_rigido} u.c.")
    print(f"Perdas Modelo Bio-Inspirado: {perdas_bio} u.c.")
    
    if perdas_rigido > 0:
        reducao = ((perdas_rigido - perdas_bio) / perdas_rigido) * 100
        print(f"Eficiência do Algoritmo:     {reducao:.2f}% de redução nas perdas")
    print("=====================================================================\n")

if __name__ == "__main__":
    executar_poc_detalhada()