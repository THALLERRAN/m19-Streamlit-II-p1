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

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Configuração da Página ---
st.set_page_config(
    page_title="Análise de Dados Bancários",
    page_icon="📊",
    layout="wide"
)

# --- Título ---
st.title('📊 Análise Interativa de Dados Bancários')

# --- Carregamento e Cache dos Dados ---
# Usar o cache do Streamlit acelera o recarregamento da página
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path, delimiter=';')
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado em: {file_path}. Verifique o caminho.")
        return None

bank_raw = load_data("bank-additional-full.csv")

# --- Barra Lateral de Filtros ---
if bank_raw is not None:
    st.sidebar.header('Filtros Interativos')

    # Filtro de Idade
    min_age = int(bank_raw['age'].min())
    max_age = int(bank_raw['age'].max())
    idades = st.sidebar.slider(
        'Selecione a faixa de idade',
        min_age, max_age, (min_age, max_age)
    )

    # Filtro de Profissão
    jobs_list = bank_raw['job'].unique()
    job_filter = st.sidebar.multiselect(
        'Selecione as profissões',
        options=list(jobs_list),
        default=list(jobs_list)
    )

    # --- Aplicação dos Filtros ---
    bank_filtered = bank_raw[
        (bank_raw['age'] >= idades[0]) &
        (bank_raw['age'] <= idades[1]) &
        (bank_raw['job'].isin(job_filter))
    ]

    # --- Conteúdo Principal ---
    st.header('Visualização dos Dados')
    st.write('Use os filtros na barra lateral para explorar o conjunto de dados.')

    st.subheader('Dados Filtrados')
    st.dataframe(bank_filtered)

    # --- Gráficos Comparativos ---
    st.header('Análise Gráfica')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Proporção de Inscrições (Dados Brutos)')
        bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True).to_frame() * 100
        fig, ax = plt.subplots()
        sns.barplot(x=bank_raw_target_perc.index, y='y', data=bank_raw_target_perc, ax=ax)
        ax.bar_label(ax.containers[0], fmt='%.2f%%')
        st.pyplot(fig)

    with col2:
        st.subheader('Proporção de Inscrições (Dados Filtrados)')
        if not bank_filtered.empty:
            bank_target_perc = bank_filtered['y'].value_counts(normalize=True).to_frame() * 100
            fig, ax = plt.subplots()
            sns.barplot(x=bank_target_perc.index, y='y', data=bank_target_perc, ax=ax)
            ax.bar_label(ax.containers[0], fmt='%.2f%%')
            st.pyplot(fig)
        else:
            st.warning("Nenhum dado corresponde aos filtros selecionados.")


    # --- SEÇÃO DE DOWNLOAD ---
    st.header('⬇️ Download dos Dados Filtrados')
    st.write('Clique em um dos botões abaixo para baixar o arquivo CSV com os dados atuais da tabela.')

    # Converte o dataframe para CSV para ser baixado
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False, sep=';').encode('utf-8')

    csv = convert_df_to_csv(bank_filtered)

    # Botão de download padrão
    st.download_button(
       label="Baixar como CSV (Padrão)",
       data=csv,
       file_name='bank_filtered.csv',
       mime='text/csv',
    )

    # Botão de download com emoji
    st.download_button(
       label="Baixar com Emoji",
       data=csv,
       file_name='bank_filtered.csv',
       mime='text/csv',
       icon="📥"
    )

    # Botão de download com ícone do Material Symbols
    st.download_button(
       label="Baixar com Ícone Material",
       data=csv,
       file_name='bank_filtered.csv',
       mime='text/csv',
       icon=":material/download:"
    )