# 📌 PoC Dinâmica: Redes Computacionais Simbióticas via Anastomose em MAS

Este repositório contém a Prova de Conceito (PoC) desenvolvida para avaliar o impacto de um algoritmo descentralizado inspirado no fenômeno biológico da **Anastomose** aplicado a **Sistemas Multiagentes (MAS)**. O objetivo principal é mitigar a perda de requisições em nós de processamento distribuído sob cenários de estresse e carga volátil.

---

## 📌 Cenário e Problema

Em arquiteturas rígidas tradicionais, os nós de processamento operam de forma isolada. Quando um nó atinge o limite de sua capacidade física (estouro de carga), o tráfego excedente é imediatamente descartado (*packet drop*), gerando perdas, mesmo que os nós vizinhos na mesma malha estejam ociosos.

**A Solução:** Inspirado na fusão de canais biológicos (como as de hifas fúngicas), este ecossistema permite que nós sobrecarregados estabeleçam **conexões lógicas temporárias e descentralizadas** com nós vizinhos que possuam folga computacional, escoando o fluxo de dados e aumentando a resiliência global do sistema.

---

## Arquitetura do Software e Classes

O projeto foi construído utilizando o ecossistema **Mesa** (framework Python para modelagem baseada em agentes) e está dividido em componentes principais que interagem dinamicamente:

              ┌──────────────────────────────┐
              │           main.py            │
              │         (Executável)         │
              └──────────────┬───────────────┘
                             │ instância
                             ▼
              ┌──────────────────────────────┐
              │          modelo.py           │
              │   (MalhaComputacionalModel)  │
              └──────────────┬───────────────┘
                             │ gerenciamento
                             ▼
              ┌──────────────────────────────┐
              │          agente.py           │
              │   (NoProcessamentoAgente)    │
              └──────────────────────────────┘


### 1. `NoProcessamentoAgente` (em `agente.py`)
Representa a unidade computacional individual (o hardware) configurada em uma topologia de malha completa (*fully connected*).
* **Atributos Principais:** `capacidade_total` (fixada em 100 u.c.), `carga_atual`, `indice_saude` ($Is$) e `requisicoes_perdidas`.
* **Mecanismo de Saúde:** O agente calcula seu índice de saúde através da fórmula:
  $$Is = \frac{\text{capacidade\_total} - \text{carga\_atual}}{\text{capacidade\_total}}$$
  Se $Is < 0$, o nó encontra-se em estado de sobrecarga/déficit.
* **Protocolo de Anastomose (Fase de Fusão):** Ao entrar em déficit com a anastomose ativa, o agente varre a malha, localiza o parceiro com a maior folga computacional disponível e transfere dinamicamente o excedente de carga ($\min(\text{deficit}, \text{maior\_folga})$).

### 2. `MalhaComputacionalModel` (em `modelo.py`)
Representa o ambiente de rede que encapsula e coordena o ciclo de vida dos agentes.
* **Função:** Instancia os 4 nós de processamento e, a cada ciclo temporal (`step`), simula a volatilidade do mundo real injetando cargas aleatórias (entre 0 e 160 u.c.) na malha sob uma ordenação estrita. Ele gerencia se a flag `anastomose_ativa` está ligada ou desligada.

### 3. Scripts de Execução e Automação
* **`main.py`:** Motor de execução inicial para visualização em tempo real das logs no terminal de ambos os cenários (Rígido vs Simbiótico).
* **`batch_run.py`:** Automatizador para simulações em larga escala. Executa um experimento estatístico de Monte Carlo processando **100.000 sementes (seeds)** consecutivas para validação empírica e gera o dataset `resultados_poc_larga_escala.csv`.
* **`analise_dados.py`:** Script focado em Data Science que consome o CSV gerado, calcula métricas estatísticas macro (média global, consistência) e plota gráficos analíticos de distribuição de eficiência e dispersão de perdas (Boxplot).

---

## 📌 Rigor Metodológico

Para garantir a validade científica exigida pela banca, este experimento adota estritamente o princípio do **Determinismo Pseudoaleatório (PRNG)** através do congelamento e controle de sementes matemáticas (`random.seed(seed)`), isolando o fator arquitetural (*Ceteris Paribus*). Na automação de larga escala, a PoC é estressada por uma amostragem maciça de 100.000 cenários probabilísticos distintos.

---

## Como Executar o Projeto 

Esta seção descreve os comandos necessários para clonar o repositório, configurar o ambiente virtual, instalar as dependências e executar a simulação.

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.10** (ou superior) e o gerenciador de pacotes `pip` instalados em sua máquina.

### 2. Configuração e Execução (Windows PowerShell)

Abra o terminal na pasta raiz do projeto e execute os comandos abaixo para preparar o ambiente virtual, instalar as dependências e rodar a arquitetura completa:

```powershell
# 1. Liberar a Execução de Scripts no PowerShell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 2. Criação do ambiente virtual
python -m venv .venv

# 3. Ativação do ambiente virtual
.venv\Scripts\Activate.ps1

# 4. Atualização do gerenciador de pacotes e instalação das dependências
pip install --upgrade pip
pip install mesa pandas matplotlib seaborn

# 5. Execução da Implementação Inicial
python main.py

# 6. Execução da Simulação de Estatísticas Massivas (100.000 Seeds)
python batch_run.py

# 7. Geração de Análise de Dados e Gráficos 
python analise_dados.py