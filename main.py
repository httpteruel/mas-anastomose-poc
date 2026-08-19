import random
from modelo import MalhaComputacionalModel

def executar_poc(semente=42, ciclos=100):
    print("=====================================================================")
    print(f"       INICIANDO POC {semente})")
    print("=====================================================================\n")

    # Cenário A
    random.seed(semente)
    modelo_rigido = MalhaComputacionalModel(anastomose_ativa=False)
    for _ in range(ciclos):
        modelo_rigido.step()
    perdas_rigido = sum([a.requisicoes_perdidas for a in modelo_rigido.agents])

    # Cenário B
    random.seed(semente)
    modelo_bio = MalhaComputacionalModel(anastomose_ativa=True)
    for _ in range(ciclos):
        modelo_bio.step()
    perdas_bio = sum([a.requisicoes_perdidas for a in modelo_bio.agents])

    print(f"Perdas Modelo Rígido: {perdas_rigido} u.c.")
    print(f"Perdas Modelo Bio-Inspirado: {perdas_bio} u.c.")
    reducao = ((perdas_rigido - perdas_bio) / perdas_rigido) * 100
    print(f"Eficiência do Algoritmo: {reducao:.2f}% de redução nas perdas\n")

if __name__ == "__main__":
    executar_poc()