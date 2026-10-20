import random
from mesa import Agent

class Mensagem:
    """Representa um pacote de dados ou sinalização em trânsito no meio físico."""
    def __init__(self, tipo, emissor_id, receptor_id, conteudo, latencia_residual):
        self.tipo = tipo  # 'REQUEST', 'ACK', 'TRANSFER'
        self.emissor_id = emissor_id
        self.receptor_id = receptor_id
        self.conteudo = conteudo  # ex: {'folga': float} ou {'carga': float}
        self.latencia_residual = latencia_residual


class NoProcessamentoAgente(Agent):
    def __init__(self, identificador_unico, modelo, capacidade_total, 
                 cap_canal=50.0, latencia_media=1, prob_perda=0.02, timeout=2, max_buffer_factor=1.5):
        super().__init__(modelo)
        self.unique_id = identificador_unico
        self.capacidade_total = capacidade_total
        self.carga_atual = 0.0
        self.indice_saude = 1.0
        self.requisicoes_perdidas = 0.0
        
        # --- Parâmetros de Restrição de Rede ---
        self.cap_canal = cap_canal             # Cap_canal: Vazão máxima do enlace por ciclo
        self.latencia_media = latencia_media   # \delta_t: Latência média de propagação
        self.prob_perda = prob_perda           # p_loss: Probabilidade de drop no canal
        self.timeout = timeout                 # T_out: Janela de tolerância para resposta
        
        # Buffer máximo tolerado antes do drop imediato de injeção
        self.buffer_maximo = capacidade_total * max_buffer_factor
        
        # Caixas de Mensagens e Estado Assíncrono
        self.inbox = []
        self.mensagens_em_transito = []
        self.negociacao_ativa = None

    def calcular_saude(self):
        if self.capacidade_total == 0:
            self.indice_saude = 0.0
            return
        self.indice_saude = (self.capacidade_total - self.carga_atual) / self.capacidade_total

    def buscar_vizinhos_topologicos(self):
        """Retorna os nós vizinhos adjacentes na grade."""
        if hasattr(self.model, 'grid') and self.model.grid is not None:
            if hasattr(self, 'pos') and self.pos is not None:
                vizinhos_coords = self.model.grid.get_neighborhood(
                    self.pos, moore=False, include_center=False
                )
                agentes_vizinhos = []
                for coord in vizinhos_coords:
                    agentes_vizinhos.extend(self.model.grid.get_cell_list_contents([coord]))
                return sorted(agentes_vizinhos, key=lambda a: a.unique_id)
        
        return [a for a in self.model.agents if a.unique_id != self.unique_id]

    def enviar_mensagem(self, receptor, tipo, conteudo):
        """Simula a transmissão do pacote sujeita a perda e atraso."""
        if random.random() < self.prob_perda:
            return  # Pacote descartado por interferência de rede
            
        latencia = max(1, int(random.expovariate(1.0 / self.latencia_media))) if self.latencia_media > 0 else 1
        
        msg = Mensagem(
            tipo=tipo,
            emissor_id=self.unique_id,
            receptor_id=receptor.unique_id,
            conteudo=conteudo,
            latencia_residual=latencia
        )
        self.mensagens_em_transito.append((receptor, msg))

    def avançar_transito_mensagens(self):
        """Decrementa a latência e entrega pacotes maduros na inbox dos receptores."""
        restantes = []
        for receptor, msg in self.mensagens_em_transito:
            msg.latencia_residual -= 1
            if msg.latencia_residual <= 0:
                receptor.inbox.append(msg)
            else:
                restantes.append((receptor, msg))
        self.mensagens_em_transito = restantes

    def processar_inbox(self):
        """Processa mensagens recebidas na caixa de entrada."""
        mensagens = list(self.inbox)
        self.inbox.clear()

        for msg in mensagens:
            emissor = next((a for a in self.model.agents if a.unique_id == msg.emissor_id), None)
            if not emissor:
                continue

            if msg.tipo == 'REQUEST':
                # Folga real considerando capacidade total e carga atual
                folga = max(0.0, self.capacidade_total - self.carga_atual)
                if folga > 0:
                    self.enviar_mensagem(emissor, 'ACK', {'folga': folga})

            elif msg.tipo == 'ACK':
                if self.negociacao_ativa:
                    self.negociacao_ativa['ofertas'].append({
                        'emissor': emissor,
                        'folga': msg.conteudo.get('folga', 0.0)
                    })

            elif msg.tipo == 'TRANSFER':
                carga_recebida = msg.conteudo.get('carga', 0.0)
                # Aceita o fluxo e descarta apenas o que estourar o buffer físico total
                self.carga_atual += carga_recebida
                if self.carga_atual > self.buffer_maximo:
                    excedente = self.carga_atual - self.buffer_maximo
                    self.requisicoes_perdidas += excedente
                    self.carga_atual = self.buffer_maximo

    def executar_anastomose_assincrona(self):
        """Gerencia o protocolo de escoamento e controle de sobrecarga."""
        deficit = self.carga_atual - self.capacidade_total
        if deficit <= 0:
            self.negociacao_ativa = None
            return

        # FASE 1: Disparo de requisições de auxílio
        if self.negociacao_ativa is None:
            vizinhos = self.buscar_vizinhos_topologicos()
            if not vizinhos:
                self.requisicoes_perdidas += deficit
                self.carga_atual = self.capacidade_total
                return

            self.negociacao_ativa = {
                'deficit_inicial': deficit,
                'ciclos_espera': 0,
                'ofertas': []
            }
            
            # Limita a solicitação ao teto do canal
            solicitacao = min(deficit, self.cap_canal)
            for vizinho in vizinhos:
                self.enviar_mensagem(vizinho, 'REQUEST', {'deficit': solicitacao})
            return

        # FASE 2: Avaliação de respostas e efetivação da transferência
        self.negociacao_ativa['ciclos_espera'] += 1
        ofertas = self.negociacao_ativa['ofertas']
        tempo_espera = self.negociacao_ativa['ciclos_espera']

        if ofertas or tempo_espera >= self.timeout:
            if ofertas:
                melhor_oferta = max(ofertas, key=lambda x: x['folga'])
                parceiro = melhor_oferta['emissor']
                folga_disponivel = melhor_oferta['folga']

                deficit_atual = max(0.0, self.carga_atual - self.capacidade_total)
                quantidade_transferida = min(deficit_atual, folga_disponivel, self.cap_canal)

                if quantidade_transferida > 0:
                    self.carga_atual -= quantidade_transferida
                    self.enviar_mensagem(parceiro, 'TRANSFER', {'carga': quantidade_transferida})

            # Truncamento de estouro de buffer (drop apenas do excedente insustentável)
            if self.carga_atual > self.buffer_maximo:
                excedente = self.carga_atual - self.buffer_maximo
                self.requisicoes_perdidas += excedente
                self.carga_atual = self.buffer_maximo

            self.negociacao_ativa = None

    def step(self):
        # 1. Transita pacotes pendentes no meio físico e atende mensagens recebidas
        self.avançar_transito_mensagens()
        self.processar_inbox()
        self.calcular_saude()

        # 2. Se houver sobrecarga, aplica a estratégia bio-inspirada ou rígida
        if self.model.anastomose_ativa:
            if self.indice_saude < 0:
                self.executar_anastomose_assincrona()
        else:
            # Modelo Rígido: Drop imediato do excedente sobre a capacidade
            if self.carga_atual > self.capacidade_total:
                excedente = self.carga_atual - self.capacidade_total
                self.requisicoes_perdidas += excedente
                self.carga_atual = self.capacidade_total

        # 3. Processamento Local (consumo da carga retida pela capacidade de processamento do nó)
        self.carga_atual = max(0.0, self.carga_atual - self.capacidade_total)
        self.calcular_saude()