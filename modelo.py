import random
from mesa import Model
from mesa.space import MultiGrid
from agente import NoProcessamentoAgente

class MalhaComputacionalModel(Model):
    def __init__(self, anastomose_ativa=True):
        super().__init__()
        self.grid = MultiGrid(2, 2, torus=False)
        self.anastomose_ativa = anastomose_ativa
        self.ciclo_atual = 0
        
        id_no = 0
        for x in range(2):
            for y in range(2):
                no = NoProcessamentoAgente(
                    identificador_unico=id_no, 
                    modelo=self, 
                    capacidade_total=100,
                    cap_canal=50.0,      # Padronizado para 50.0 u.c. conforme o artigo
                    latencia_media=1,    # Latência Poisson/Exponencial de 1 ciclo
                    prob_perda=0.02,     # 2% de probabilidade de falha no enlace
                    timeout=2            # Janela de timeout
                )
                self.grid.place_agent(no, (x, y))
                self.agents.add(no)
                id_no += 1

    def obter_total_perdas(self):
        return sum([agente.requisicoes_perdidas for agente in self.agents])

    def step(self):
        self.ciclo_atual += 1
        agentes_ordenados = sorted(list(self.agents), key=lambda a: a.unique_id)
        
        # Injeção estocástica de carga externa [0, 160] u.c.
        for agente in agentes_ordenados:
            carga_injetada = random.randint(0, 160)
            
            agente.carga_atual = min(150.0, agente.carga_atual + carga_injetada)
            
        for agente in agentes_ordenados:
            agente.step()