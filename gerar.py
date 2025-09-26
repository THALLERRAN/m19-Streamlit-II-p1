# -*- coding: utf-8 -*-
# CÓDIGO CORRIGIDO PARA FUNCIONAR COM STREAMLIT

# 1. Importações
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Configuração da Página do Streamlit ---
st.set_page_config(
    page_title="Dashboard de Análise Bancária",
    layout="wide" # Usa o layout mais largo da página
)

st.title("Análise de Campanha Bancária")

# --- Carregamento dos Dados ---
# Usamos @st.cache_data para otimizar o carregamento do arquivo
@st.cache_data
def carregar_dados():
    try:
        bank_raw = pd.read_csv("bank-additional-full.csv", sep=';')
        return bank_raw
    except FileNotFoundError:
        st.error("Erro: Arquivo 'bank-additional-full.csv' não foi encontrado.")
        return None

bank_raw = carregar_dados()

# Só executa o resto do app se os dados foram carregados com sucesso
if bank_raw is not None:
    bank = bank_raw.copy()

    # --- Barra Lateral com Filtros ---
    st.sidebar.header("Filtros Interativos")

    # Slider para selecionar a faixa de idade
    min_age = int(bank['age'].min())
    max_age = int(bank['age'].max())

    idades = st.sidebar.slider(
        'Selecione a faixa de idade:',
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age) # Valor inicial (range completo)
    )

    # --- Lógica de Negócio e Filtragem ---
    # Filtra o dataframe principal com base na seleção do slider
    bank_filtrado = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]

    # --- Exibição dos Gráficos e Dados na Página Principal ---

    st.header(f"Análise para a faixa de idade: {idades[0]} a {idades[1]} anos")

    # Calcula as proporções para os gráficos
    bank_target_perc_bruto = bank_raw['y'].value_counts(normalize=True).to_frame('proportion') * 100
    bank_target_perc_bruto = bank_target_perc_bruto.sort_index()

    bank_target_perc_filtrado = bank_filtrado['y'].value_counts(normalize=True).to_frame('proportion') * 100
    bank_target_perc_filtrado = bank_target_perc_filtrado.sort_index()

    # Criação da figura para os plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Dados Brutos
    sns.barplot(x=bank_target_perc_bruto.index,
                y='proportion',
                data=bank_target_perc_bruto,
                ax=ax1)
    ax1.bar_label(ax1.containers[0], fmt='%.2f%%')
    ax1.set_title('Dados Completos (População Total)', fontweight="bold")
    ax1.set_ylabel('Proporção (%)')
    ax1.set_xlabel('Resultado (y)')

    # Plot 2: Dados Filtrados
    sns.barplot(x=bank_target_perc_filtrado.index,
                y='proportion',
                data=bank_target_perc_filtrado,
                ax=ax2)
    ax2.bar_label(ax2.containers[0], fmt='%.2f%%')
    ax2.set_title(f'Dados Filtrados por Idade', fontweight="bold")
    ax2.set_ylabel('Proporção (%)')
    ax2.set_xlabel('Resultado (y)')
    
    fig.suptitle('Comparação da Proporção de Sucesso da Campanha', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Exibe o gráfico no Streamlit usando st.pyplot()
    st.pyplot(fig)
    
    st.markdown("---") # Adiciona uma linha divisória

    # Exibe a tabela de dados filtrados usando st.dataframe()
    st.header("Amostra dos Dados Filtrados")
    st.dataframe(bank_filtrado.head())