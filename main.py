import random
from modelo import MalhaComputacionalModel

def gerar_cenario_cargas(semente=42, ciclos=100, num_agentes=4):
    """
    Garante que exatamente o mesmo padrão de tráfego/carga seja 
    gerado para ambos os modelos em todos os ciclos.
    """
    random.seed(semente)
    cenario = []
    for _ in range(ciclos):
        # Gera carga estocástica no intervalo nominal [0, 160] u.c.
        cargas_ciclo = [random.randint(0, 160) for _ in range(num_agentes)]
        cenario.append(cargas_ciclo)
    return cenario

def executar_poc_detalhada(semente=42, ciclos=100):
    print("=====================================================================")
    print(f"         INICIANDO POC (SEMENTE {semente})")
    print("=====================================================================\n")

    # Pré-gera o histórico exato de tráfego para os 100 ciclos
    historico_cargas = gerar_cenario_cargas(semente=semente, ciclos=ciclos)

    # --- CENÁRIO A: MODELO RÍGIDO
    print("--- [RUNDOWN] CENÁRIO A: MODELO RÍGIDO ---")
    modelo_rigido = MalhaComputacionalModel(anastomose_ativa=False)
    
    for ciclo in range(1, ciclos + 1):
        cargas_inj = historico_cargas[ciclo - 1]
        
        agentes_ordenados = sorted(list(modelo_rigido.agents), key=lambda a: a.unique_id)
        
        # Injeta as cargas nos nós  respeitando a ausência de buffer no Cenário Rígido
        for i, agente in enumerate(agentes_ordenados):
            agente.carga_atual = cargas_inj[i]

        # Executa o ciclo de processamento
        modelo_rigido.step_sem_injecao_interna() if hasattr(modelo_rigido, 'step_sem_injecao_interna') else None
        
        # Executa a lógica dos agentes
        for agente in agentes_ordenados:
            agente.step()
        
        perdas_acumuladas = sum([a.requisicoes_perdidas for a in modelo_rigido.agents])
        print(f"Ciclo {ciclo:03d} | Cargas Injetadas (Nós 0-3): {cargas_inj} | Perdas Acumuladas: {perdas_acumuladas} u.c.")

    perdas_rigido = sum([a.requisicoes_perdidas for a in modelo_rigido.agents])

    print("\n" + "="*70 + "\n")

    # --- CENÁRIO B: MODELO BIO-INSPIRADO
    print("--- [RUNDOWN] CENÁRIO B: MODELO BIO-INSPIRADO ---")
    modelo_bio = MalhaComputacionalModel(anastomose_ativa=True)

    for ciclo in range(1, ciclos + 1):
        cargas_inj = historico_cargas[ciclo - 1]
        
        agentes_ordenados = sorted(list(modelo_bio.agents), key=lambda a: a.unique_id)
        
        for i, agente in enumerate(agentes_ordenados):
            agente.carga_atual = min(150.0, agente.carga_atual + cargas_inj[i])

        # Executa a lógica dos agentes
        for agente in agentes_ordenados:
            agente.step()
        
        perdas_acumuladas = sum([a.requisicoes_perdidas for a in modelo_bio.agents])
        print(f"Ciclo {ciclo:03d} | Cargas Injetadas (Nós 0-3): {cargas_inj} | Perdas Acumuladas: {perdas_acumuladas} u.c.")

    perdas_bio = sum([a.requisicoes_perdidas for a in modelo_bio.agents])

    # --- EXIBIÇÃO DOS RESULTADOS
    print("\n=====================================================================")
    print("                           RESULTADOS                              ")
    print("=====================================================================")
    print(f"Perdas Modelo Rígido:        {perdas_rigido} u.c.")
    print(f"Perdas Modelo Bio-Inspirado: {perdas_bio} u.c.")
    
    if perdas_rigido > 0:
        reducao = ((perdas_rigido - perdas_bio) / perdas_rigido) * 100
        print(f"Eficiência do Algoritmo:     {reducao:.2f}% de redução nas perdas")
    print("=====================================================================\n")

if __name__ == "__main__":
    executar_poc_detalhada()