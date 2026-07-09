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
                no = NoProcessamentoAgente(id_no, self, capacidade_total=100)
                self.grid.place_agent(no, (x, y))
                self.agents.add(no)
                id_no += 1

    def obter_total_perdas(self):
        return sum([agente.requisicoes_perdidas for agente in self.agents])

    def step(self):
        self.ciclo_atual += 1
        
        agentes_ordenados = sorted(list(self.agents), key=lambda a: a.unique_id)
        
        for agente in agentes_ordenados:
            agente.carga_atual = random.randint(0, 160)
            
        for agente in agentes_ordenados:
            agente.step()