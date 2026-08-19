from mesa import Agent

class NoProcessamentoAgente(Agent):
    def __init__(self, identificador_unico, modelo, capacidade_total):
        super().__init__(modelo)
        self.unique_id = identificador_unico 
        self.capacidade_total = capacity_total = capacidade_total
        self.carga_atual = 0
        self.indice_saude = 1.0
        self.requisicoes_perdidas = 0

    def calcular_saude(self):
        if self.capacidade_total == 0:
            self.indice_saude = 0
            return
        self.indice_saude = (self.capacidade_total - self.carga_atual) / self.capacidade_total

    def buscar_vizinhos(self):

        vizinhos = [agente for agente in self.model.agents if agente.unique_id != self.unique_id]
        return sorted(vizinhos, key=lambda a: a.unique_id)

    def executar_anastomose(self):
        deficit = self.carga_atual - self.capacidade_total
        if deficit <= 0:
            return

        vizinhos = self.buscar_vizinhos()
        melhor_vizinho = None
        maior_folga = 0

        for vizinho in vizinhos:
            folga_vizinho = vizinho.capacidade_total - vizinho.carga_atual
            if folga_vizinho > maior_folga:
                maior_folga = folga_vizinho
                melhor_vizinho = vizinho

        if melhor_vizinho:
            quantidade_transferida = min(deficit, maior_folga)
            self.carga_atual -= quantidade_transferida
            melhor_vizinho.carga_atual += quantidade_transferida
            
            novo_deficit = self.carga_atual - self.capacidade_total
            if novo_deficit > 0:
                self.requisicoes_perdidas += novo_deficit
                self.carga_atual = self.capacidade_total
        else:
            self.requisicoes_perdidas += deficit
            self.carga_atual = self.capacidade_total

    def step(self):
        self.calcular_saude()
        
        if self.model.anastomose_ativa and self.indice_saude < 0:
            self.executar_anastomose()
        elif self.indice_saude < 0:
            deficit = self.carga_atual - self.capacidade_total
            self.requisicoes_perdidas += deficit
            self.carga_atual = self.capacidade_total