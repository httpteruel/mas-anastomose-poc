import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_resultados():

    arquivo = "resultados_poc_larga_escala.csv"
    df = pd.read_csv(arquivo)
    
    print("=====================================================================")
    print("           ANÁLISE DE DADOS - RESULTADOS POC MAS ANASTOMOSE")
    print("=====================================================================\n")
    
    total_seeds = len(df)
    media_rigido = df['Perdas_Rigido'].mean()
    media_bio = df['Perdas_Bio_Inspirado'].mean()
    media_reducao = df['Reducao_Percentual'].mean()
    
    # COMPARATIVO
    vitorias_bio = df[df['Perdas_Bio_Inspirado'] < df['Perdas_Rigido']].shape[0]
    percentual_vitorias = (vitorias_bio / total_seeds) * 100
    
    print(f"Total de Cenários Analisados: {total_seeds:,}".replace(",", "."))
    print(f"Média de perdas no modelo Rígido: {media_rigido:.2f} u.c.")
    print(f"Média de perdas no modelo Bio-Inspirado: {media_bio:.2f} u.c.")
    print(f"Eficiência Média Global: O algoritmo bio-inspirado reduziu as perdas em {media_reducao:.2f}%")
    print(f"Consistência: O algoritmo superou o modelo rígido em {percentual_vitorias:.2f}% das seeds utilizadas.")
    print("=====================================================================\n")

    sns.set_theme(style="whitegrid")
    
    # --- GRÁFICO 1: Histograma (Aumentado para 12x7 polegadas) ---
    plt.figure(figsize=(12, 7))
    sns.histplot(df['Reducao_Percentual'], bins=50, kde=True, color='forestgreen')
    plt.axvline(media_reducao, color='red', linestyle='--', linewidth=2, label=f'Média ({media_reducao:.2f}%)')
    plt.title('Distribuição da Eficiência do Algoritmo Bio-Inspirado\n(100.000 Sementes Simuladas)', fontsize=16, pad=15)
    plt.xlabel('Redução das Perdas de Carga (%)', fontsize=14)
    plt.ylabel('Frequência (Número de Sementes)', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig('distribuicao_eficiencia.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("-> Gráfico 'distribuicao_eficiencia.png' gerado com sucesso (Tamanho ampliado)!")

    # --- GRÁFICO 2: Boxplot (Aumentado para 12x7 polegadas) ---
    df_melted = pd.melt(df, value_vars=['Perdas_Rigido', 'Perdas_Bio_Inspirado'], 
                        var_name='Arquitetura', value_name='Perdas')
    df_melted['Arquitetura'] = df_melted['Arquitetura'].map({
        'Perdas_Rigido': 'Rígida Tradicional', 
        'Perdas_Bio_Inspirado': 'Bio-Inspirada'
    })

    plt.figure(figsize=(12, 7))

    sns.boxplot(x='Arquitetura', y='Perdas', hue='Arquitetura', data=df_melted, 
                palette=['#cf142b', '#228b22'], legend=False, width=0.4)
    plt.title('Comparativo de Dispersão de Perdas Totais por Arquitetura', fontsize=16, pad=15)
    plt.xlabel('Tipo de Arquitetura de Rede', fontsize=14)
    plt.ylabel('Volume de Cargas Perdidas (u.c.)', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=11)
    plt.tight_layout()
    plt.savefig('comparativo_boxplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("-> Gráfico 'comparativo_boxplot.png' gerado com sucesso (Tamanho ampliado)!")
    print("=====================================================================")

if __name__ == "__main__":
    analisar_resultados()